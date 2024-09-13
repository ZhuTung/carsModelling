from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import car_generation.carGen as cargen
import car_generation.carSql as carsql

def insert_data(table_name, values):

    placeholders = ', '.join(['%s'] * len(values))

    query = f"INSERT INTO {table_name} VALUES ({placeholders})"

    pg_hook = PostgresHook(postgres_conn_id='carsdb')

    pg_hook.run(query, parameters=values)

    print(f"Data inserted into {table_name} successfully.")

def calculate(values, discount, commision):
    custom_keys = ['transactionid','paymentid','dateid','carid','sellerid','customerid','factoryid','totaladj','profit']

    transid = cargen.generate_ID()
    totaladj = discount + commision
    totaladj = round(totaladj, 2)
    profit = 10.8

    values = (transid,) + values + (totaladj, profit)

    result = {custom_keys[i]: values[i] for i in range(len(values))}

    return result

# HANLDE ALL THE DAGS HERE
with DAG(
    dag_id='cars',
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    description="My first DAG for cars",
    catchup=False
) as dag: 
    
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='carsdb',
        sql=carsql.create_tables
    )

    payment = PythonOperator(
        task_id='payment',
        python_callable=cargen.generate_payment,
        multiple_outputs=True
    )

    date = PythonOperator(
        task_id='date',
        python_callable=cargen.generate_date,
        multiple_outputs=True
    )

    car = PythonOperator(
        task_id='car',
        python_callable=cargen.generate_car,
        multiple_outputs=True
    )

    seller = PythonOperator(
        task_id='seller',
        python_callable=cargen.generate_seller,
        multiple_outputs=True
    )

    customer = PythonOperator(
        task_id='customer',
        python_callable=cargen.generate_customer,
        multiple_outputs=True
    )
    
    company = PythonOperator(
        task_id='factory',
        python_callable=cargen.generate_company,
        multiple_outputs=True
    )

    insert_payment = PythonOperator(
        task_id='insert_payment',
        python_callable=insert_data,
        op_args=['D_Payment', (
            payment.output["id"],
            payment.output["plan"],
            payment.output["cardtype"],
            payment.output["cardNum"],
            payment.output["amt"],
            payment.output["status"],
            payment.output["date"],
            payment.output["installNum"],
            payment.output["totalInstall"],
            payment.output["invoiceID"],
            payment.output["discount"],
            payment.output["confirmNum"]
        )]
    )

    insert_date = PythonOperator(
        task_id='insert_date',
        python_callable=insert_data,
        op_args=['D_Date', (
            date.output["id"],
            date.output["sDate"],
            date.output["sTime"],
            date.output["sDay"],
            date.output["fMonth"],
            date.output["fYear"],
            date.output["pDate"]
        )]
    )

    insert_car = PythonOperator(
        task_id='insert_car',
        python_callable=insert_data,
        op_args=['D_Car', (
            car.output["id"],
            car.output["brand"],
            car.output["model"],
            car.output["seat"],
            car.output["plate"],
            car.output["vol"],
            car.output["manuDt"],
            car.output["hp"],
            car.output["color"],
            car.output["iPrice"],
            car.output["sPrice"]
        )]
    )

    insert_seller = PythonOperator(
        task_id='insert_seller',
        python_callable=insert_data,
        op_args=['D_Seller', (
            seller.output["id"],
            seller.output["fname"],
            seller.output["lname"],
            seller.output["phoneNum"],
            seller.output["yos"],
            seller.output["commision"]
        )]
    )

    insert_customer = PythonOperator(
        task_id='insert_customer',
        python_callable=insert_data,
        op_args=['D_Customer', (
            customer.output["id"],
            customer.output["fname"],
            customer.output["lname"],
            customer.output["phoneNum"],
            customer.output["address"],
            customer.output["city"],
            customer.output["state"],
            customer.output["pcode"],
            customer.output["country"]
        )]
    )

    insert_factory = PythonOperator(
        task_id='insert_factory',
        python_callable=insert_data,
        op_args=['D_Factory', (
            company.output["id"],
            company.output["facName"],
            company.output["address"],
            company.output["city"],
            company.output["state"],
            company.output["pcode"],
            company.output["country"],
            company.output["brand"],
            company.output["phoneNum"],
            company.output["phoneCode"],
            company.output["fname"],
            company.output["lname"]
        )]
    )

    cal_trans = PythonOperator(
        task_id='cal_trans',
        python_callable=calculate,
        op_args=[(
            payment.output["id"],
            date.output["id"],
            car.output["id"],
            seller.output["id"],
            customer.output["id"],
            company.output["id"]
        ), payment.output["discount"], seller.output["commision"]],
        multiple_outputs = True,
    )

    insert_transaction = PythonOperator(
        task_id='insert_transaction',
        python_callable=insert_data,
        op_args=['F_Transaction', (
            cal_trans.output["transactionid"],
            cal_trans.output["dateid"],
            cal_trans.output["carid"],
            cal_trans.output["factoryid"],
            cal_trans.output["customerid"],
            cal_trans.output["sellerid"],
            cal_trans.output["paymentid"],
            cal_trans.output["totaladj"],
            cal_trans.output["profit"]
        )]
    )
    
    create_table >> payment >> insert_payment >> date >> insert_date >> car >> insert_car >> seller >> insert_seller >> customer >> insert_customer >> company >> insert_factory >> cal_trans >> insert_transaction