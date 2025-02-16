# E-commerce Microservices Remote Procedure Call(RPC) Communication Example

## Project description
در معماری میکروسرویس پلتفرم ایکامرس، دو سرویس برای مدیریت کاربران و ثبت سفارش خرید وجود دارد. دیتابیس پروژه MongoDB می باشد که از کتابخانه Pymongo  برای ارتباط با سرور و همچنین RabbitMQ  برای پیام رسانی بین سرویس ها استفاده شده است. ثبت نهایی هر رکورد خرید در دیتابیس نیازمند این است که  id هر کاربر از طریق سرویس کاربران دریافت بگردد و همراه اطلاعات سفارش در دیتابیس ذخیره بگردد و برای این منظور یک Remote Procedure Call را پیاده سازی شده است.

## Microservice Architecture
### 1. User Service
Required functionalities:
- Create a user (name, email, phone number)
- Retrieve user information by ID

### 2. Order Service
Required functionalities:
- Place an order (user, product name, price, quantity)
- Retrieve a list of orders for a user

Orders must be associated with the user's ID, which will be fetched from the User Service.

## Project Features
1. **Backend**: Async FastAPI
2. **API Gateway**: Used for routing requests between microservices by NGINX.
3. **Inter-Service Messaging**: Async RabbitMQ is used for communication between services by AIO_PIKA support.
4. **Database**: Async MongoDB is used, with Async PyMongo for database operations.
