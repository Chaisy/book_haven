from config.project_config import Database

class TableCreator:
    
    @staticmethod
    async def create_roles_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Roles (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),      
                Name VARCHAR (64) NOT NULL UNIQUE
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_coupons_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Coupons (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),        
                Sale INTEGER NOT NULL UNIQUE
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_users_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Users (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                Login VARCHAR (64) NOT NULL UNIQUE,
                Password VARCHAR (64) NOT NULL,
                Name VARCHAR (64) NOT NULL UNIQUE,
                RoleId UUID REFERENCES Roles (Id) ON DELETE SET NULL,
                CouponId UUID REFERENCES Coupons (Id) ON DELETE SET NULL,
                Banned BOOLEAN DEFAULT FALSE
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_carts_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Likes (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),       
                UserId UUID NOT NULL REFERENCES Users (Id) ON DELETE CASCADE,
                Books UUID[] DEFAULT '{}'
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_firms_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Rang (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),      
                Naming VARCHAR (64) NOT NULL UNIQUE
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_animals_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Status (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                Type VARCHAR (64) NOT NULL UNIQUE
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_categories_of_good_table():
        query = '''
            CREATE TABLE IF NOT EXISTS CategoriesOfGood (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                Title VARCHAR(64) NOT NULL UNIQUE
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_goods_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Books (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
                Title VARCHAR (64) NOT NULL,
                RangId UUID REFERENCES Rang (Id) ON DELETE CASCADE,
                CategoryOfGoodId UUID REFERENCES CategoriesOfGood (Id) ON DELETE CASCADE,
                StatusId UUID REFERENCES Status (Id) ON DELETE CASCADE
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_orders_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Meets (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                UserId UUID REFERENCES Users (Id) ON DELETE SET NULL,
                Books UUID[] DEFAULT ARRAY[]::UUID[]
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_order_goods_table():
        query = '''
            CREATE TABLE IF NOT EXISTS MeetGoods (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                MeetId UUID REFERENCES Meets (Id) ON DELETE CASCADE,
                BookId UUID REFERENCES Books (Id) ON DELETE CASCADE,
                Count INTEGER NOT NULL DEFAULT 1,   
                DateTime TIMESTAMP NOT NULL, 
                UNIQUE (MeetId, BookId)
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_carts_goods_table():
        query = '''
            CREATE TABLE IF NOT EXISTS LikesBooks (
                Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                LikeId UUID REFERENCES Likes (Id) ON DELETE CASCADE,
                BookId UUID REFERENCES Books (Id) ON DELETE CASCADE,
                Count INTEGER NOT NULL DEFAULT 1,
                UNIQUE (LikeId, BookId)
            );
            '''
        await Database.execute(query)

    @staticmethod
    async def create_logging_table():
        query = '''
            CREATE TABLE IF NOT EXISTS Logs (
            Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            UserId UUID REFERENCES Users (Id) ON DELETE SET NULL,
            Role VARCHAR(255),
            Action VARCHAR(255),
            Result VARCHAR(255)
            );
            '''
        await Database.execute(query)

    
    @staticmethod
    async def create_all_tables():
        await TableCreator.create_roles_table()
        await TableCreator.create_coupons_table()
        await TableCreator.create_users_table()
        await TableCreator.create_carts_table()
        await TableCreator.create_firms_table()
        await TableCreator.create_animals_table()
        await TableCreator.create_categories_of_good_table()
        await TableCreator.create_goods_table()
        await TableCreator.create_orders_table()
        await TableCreator.create_order_goods_table()
        await TableCreator.create_carts_goods_table()
        await TableCreator.create_logging_table()
