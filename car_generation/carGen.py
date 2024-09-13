import random
from datetime import timedelta, time, datetime
from faker import Faker
from faker_vehicle import VehicleProvider

"""
CREATE ALL THE NECESSARY FUNCTIONS TO GENERATE DUMMY DATA
"""
#INITIALIZE FAKER FOR GENERATING FAKE DUMMY DATA
fake = Faker()
fake.add_provider(VehicleProvider) # pip install faker_vehicle

def generate_date_and_day():
    start_date = datetime(2000,1,1)
    end_date = datetime(2024,12,31)

    num_days = (end_date - start_date).days
    rand_days = random.randint(1, num_days)
    random_date = start_date + timedelta(days=rand_days)

    date = random_date.strftime('%Y%m%d')
    day = random_date.strftime('%A')

    return {"date":date, "day":day}

def generate_time():
    hour = random.randint(0,23)
    minute = random.randint(0,59)

    random_time = time(hour,minute)
    string_time = random_time.strftime('%H:%M')

    return string_time

def generate_ID():
    return f'{random.randint(0,99999):05}'

def generate_fname_lname():
    gen_name = fake.name()
    fname = gen_name.split(' ')[0]
    lname = gen_name.split(' ')[1]
    return fname, lname

def generate_full_address():
    gen_address = fake.street_address()
    gen_city = fake.city()
    gen_state = fake.state()
    gen_postcode = fake.postalcode()
    gen_country = fake.country()
    return gen_address, gen_city, gen_state, gen_postcode, gen_country

def generate_phonenum():
    pNum = fake.phone_number()
    pCode = fake.country_calling_code()
    return {
        "pNum": pNum,
        "pCode": pCode
    }

def generate_payplan():
    plan = ['credit card', 'cash']

    return random.choice(plan)

def generate_status():
    status = ['onhold', 'canceled', 'success']

    return random.choice(status)

def generate_card():
    gen_type = fake.credit_card_provider()
    gen_cardnum = fake.credit_card_number()
    return gen_type, gen_cardnum

def gen_amt_price():
    gen_amt = fake.pricetag()
    gen_amt = gen_amt.translate(str.maketrans("","", ",$"))
    return float(gen_amt)

def generate_discount():
    return random.randint(1000,2999)/100

def generate_conNum():
    return random.randint(10000,99999)

def generate_companyName():
    cName = fake.company()
    return cName

"""
GENERATE THE DATA FOR EACH DIMENSION
"""
# Generate Payment data
def generate_payment():
    id = generate_ID()
    plan = generate_payplan()

    if plan == 'cash':
        cardtype = ''
        cardNum = ''
    else:
        cardtype, cardNum = generate_card()
    
    amt = gen_amt_price()
    status = generate_status()
    date = generate_date_and_day()

    installNum = random.randint(100000, 999999)
    totalInstall = random.randint(1,5)
    invoiceID = generate_ID()
    discount = generate_discount()
    confirmNum = generate_conNum()

    return {
        "id": id,
        "plan": plan,
        "cardtype": cardtype,
        "cardNum": cardNum,
        "amt": amt,
        "status": status,
        "date": date["date"],
        "installNum": installNum,
        "totalInstall": totalInstall,
        "invoiceID": invoiceID,
        "discount": discount,
        "confirmNum": confirmNum
    }

# Generate Date data
def generate_date():
    id = generate_ID()
    date = generate_date_and_day()
    sTime = generate_time()
    fMonth = random.randint(1,12)
    fYear = random.randint(1970,2024)
    pDate = generate_date_and_day()
    
    return {
        "id": id,
        "sDate": date["date"],
        "sTime": sTime,
        "sDay": date["day"],
        "fMonth": fMonth,
        "fYear": fYear,
        "pDate": pDate["date"]
    }

# Generate Car data
def generate_car():
    id = generate_ID()
    brand = fake.vehicle_make()
    model = fake.vehicle_model()
    seat = random.choice([2,4])
    plate = fake.license_plate()
    vol = 250
    manuDt = generate_date_and_day()
    hp = random.randint(0,500)
    color = fake.color_name()
    iPrice = gen_amt_price()
    sPrice = gen_amt_price()
    
    return {
        "id": id,
        "brand": brand, 
        "model": model, 
        "seat" :seat, 
        "plate": plate,
        "vol": vol, 
        "manuDt": manuDt["date"],
        "hp": hp,
        "color": color,
        "iPrice": iPrice, 
        "sPrice": sPrice
    }

# Generate Seller data
def generate_seller():
    id = generate_ID()
    fname, lname = generate_fname_lname()
    phoneNum = generate_phonenum()
    yos = random.randint(1,20)
    commision = gen_amt_price()

    return {
        "id": id,
        "fname": fname,
        "lname": lname,
        "phoneNum": phoneNum["pNum"],
        "yos": yos,
        "commision": commision
    }

# Generate Customer data
def generate_customer():
    id = generate_ID()
    fname, lname = generate_fname_lname()
    phoneNum = generate_phonenum()
    address, city, state, pcode, country = generate_full_address()
    return {
        "id": id,
        "fname": fname,
        "lname": lname,
        "phoneNum": phoneNum["pNum"],
        "address": address,
        "city": city,
        "state": state,
        "pcode": pcode,
        "country": country
    }

# Generate Factory Data
def generate_company():
    id = generate_ID()
    facName = generate_companyName()
    address, city, state, pcode, country = generate_full_address()
    brand = fake.vehicle_make()
    phoneNum, phoneCode = generate_phonenum()
    fname, lname = generate_fname_lname()

    return {
        "id": id,
        "facName": facName,
        "address": address,
        "city": city,
        "state": state,
        "pcode": pcode,
        "country": country,
        "brand": brand,
        "phoneNum": phoneNum,
        "phoneCode": phoneCode,
        "fname": fname,
        "lname": lname
    }
