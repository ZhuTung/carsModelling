create_tables = """
    CREATE TABLE IF NOT EXISTS D_Payment(
        PaymentID varchar(10) PRIMARY KEY,
        PaymentPlan varchar(20),
        PaymentCardType varchar(30),
        PaymentCreditCardNum varchar(20),
        PaymentAmount decimal(18,2),
        PaymentStatus varchar(10),
        PaymentDate date,
        InstallmentNum int,
        TotalInstallment int,
        InvoiceID varchar(20),
        DiscountAmount decimal(18,2),
        PaymentConfirmationNum varchar(20)
    );

    CREATE TABLE IF NOT EXISTS D_Date(
        DateID varchar(10) PRIMARY KEY,
        SellingDate date,
        SellingTime time,
        SellingDay varchar(10),
        FiscalMonth int,
        FiscalYear int,
        PromotionDate date
    );

    CREATE TABLE IF NOT EXISTS D_Car(
        CarID varchar(10) PRIMARY KEY,
        CarBrand varchar(20),
        CarModel varchar(20),
        CarSeat int,
        CarNumPlate varchar(20),
        CarTankVolume int,
        CarManufacturingDate date,
        CarHorsepower int,
        Carcolor varchar(20),
        CarImportPrice decimal(18,2),
        CarSellingPrice decimal(18,2)
    );

    CREATE TABLE IF NOT EXISTS D_Seller(
        SellerID varchar(10) PRIMARY KEY,
        SellerFname varchar(20),
        SellerLname varchar(20),
        SellerPhoneNum varchar(30),
        SellerYOS int,
        SellerCommision decimal(18,2)
    );

    CREATE TABLE IF NOT EXISTS D_Customer(
        CustomerID varchar(10) PRIMARY KEY,
        CustomerFname varchar(20),
        CustomerLname varchar(20),
        CustomerPhoneNum varchar(40),
        CustomerAddress varchar(50),
        CustomerCity varchar(20),
        CustomerState varchar(20),
        CustomerPostcode int,
        CustomerCountry varchar(30)
    );

    CREATE TABLE IF NOT EXISTS D_Factory(
        FactoryID varchar(10) PRIMARY KEY,
        FactoryName varchar(50),
        FactoryAddress varchar(50),
        FactoryCity varchar(20),
        FactoryState varchar(20),
        FactoryPostcode int,
        FactoryCountry varchar(20),
        ManufacturingBrand varchar(20),
        FactoryPhoneCode varchar(5),
        FactoryPhoneNum varchar(20),
        FactoryOwnerFname varchar(20),
        FactoryOwnerLname varchar(20)
    );

    CREATE TABLE IF NOT EXISTS F_Transaction(
        TransactionID varchar(10) PRIMARY KEY,
        DateID varchar(10), FOREIGN KEY (DateID) REFERENCES D_Date(DateID),
        CarID varchar(10), FOREIGN KEY (CarID) REFERENCES D_Car(CarID),
        FactoryID varchar(10), FOREIGN KEY (FactoryID) REFERENCES D_Factory(FactoryID),
        CustomerID varchar(10), FOREIGN KEY (CustomerID) REFERENCES D_Customer(CustomerID),
        SellerID varchar(10), FOREIGN KEY (SellerID) REFERENCES D_Seller(SellerID),
        PaymentID varchar(10), FOREIGN KEY (PaymentID) REFERENCES D_Payment(PaymentID),
        TotalAdjustments decimal(18,2),
        ProfitGenerated decimal(18,2)
    );
"""