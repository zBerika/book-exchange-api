# წიგნის გაცვლის API (Book Exchange API)

ეს არის RESTful API უფასო წიგნების გაცვლის სერვისისთვის, აგებული Django-სა და Django REST Framework-ის გამოყენებით. რეგისტრირებულ მომხმარებლებს შეუძლიათ შესთავაზონ წიგნები და აიღონ სხვების მიერ შეთავაზებული წიგნები. არარეგისტრირებულ მომხმარებლებს შეუძლიათ დაათვალიერონ ხელმისაწვდომი წიგნების სია. (This is a RESTful API for a free book exchange service, built with Django and Django REST Framework. Registered users can offer books and take books offered by others. Unregistered users can browse the list of available books.)

## ფუნქციები (Features)

* **მომხმარებლის აუთენტიფიკაცია:** (User Authentication:)
    * რეგისტრაცია ელფოსტის საშუალებით (username, email, password). (Registration via email (username, email, password).)
    * შესვლა აუთენტიფიკაციის ტოკენის მისაღებად. (Login to obtain an authentication token.)
    * მომხმარებლის პროფილის მართვა. (User profile management.)
* **წიგნების მართვა:** (Book Management:)
    * CRUD ოპერაციები წიგნებზე (შექმნა, წაკითხვა, განახლება, წაშლა). (CRUD operations for books (Create, Read, Update, Delete).)
    * წიგნების ფილტრაცია ავტორის, ჟანრის, მდგომარეობისა და მფლობელის მიხედვით. (Filtering books by author, genre, condition, and owner.)
    * წიგნების ძებნა სათაურის, აღწერის, ავტორის და ჟანრის მიხედვით. (Searching books by title, description, author, and genre.)
    * წიგნის პოსტერების/სურათების ატვირთვა. (Uploading book posters/images.)
* **დამხმარე რესურსები:** (Supporting Resources:)
    * CRUD ოპერაციები ავტორებისთვის, ჟანრებისთვის და მდგომარეობებისთვის. (CRUD operations for Authors, Genres, and Conditions.)
* **წიგნის მიღების პროცესი:** (Book Acquisition Process:)
    * მომხმარებლებს შეუძლიათ ინტერესის გამოხატვა ხელმისაწვდომი წიგნის მიმართ. (Users can express interest in an available book.)
    * წიგნის მფლობელებს შეუძლიათ ნახონ ყველა ინტერესის მოთხოვნა მათი წიგნებისთვის. (Book owners can view all interest requests for their books.)
    * წიგნის მფლობელებს შეუძლიათ მიიღონ ერთი მოთხოვნა, რაც წიგნს მიუწვდომელს ხდის და უარყოფს სხვა მოლოდინში მყოფ მოთხოვნებს. (Book owners can accept one request, which marks the book as unavailable and rejects other pending requests.)
    * წიგნის მფლობელებს შეუძლიათ უარყონ ინდივიდუალური მოთხოვნები. (Book owners can reject individual requests.)
* **ლოკაციის ინფორმაცია:** (Location Information:)
    * წიგნები მოიცავს დეტალებს მათი მიღების ლოკაციის შესახებ. (Books include details about their pickup location.)
    * მომხმარებლებს შეუძლიათ მიუთითონ მათი ზოგადი მიღების ლოკაცია პროფილში. (Users can specify their general pickup location in their profile.)

## გამოყენებული ტექნოლოგიები (Technologies Used)

* **Backend:** Python 3.10+, Django 5.x, Django REST Framework
* **მონაცემთა ბაზა:** PostgreSQL (Docker-ით), SQLite (სწრაფი ლოკალური განვითარებისთვის) (Database: PostgreSQL (with Docker), SQLite (for quick local dev))
* **API დოკუმენტაცია:** drf-yasg (Swagger UI)
* **კონტეინერიზაცია:** Docker, Docker Compose (Containerization: Docker, Docker Compose)
* **ვერსიის კონტროლი:** Git (Version Control: Git)

## დაწყება (Getting Started)

ეს ინსტრუქციები დაგეხმარებათ პროექტის გაშვებაში თქვენს ლოკალურ მანქანაზე განვითარებისა და ტესტირების მიზნით. (These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.)

### წინაპირობები (Prerequisites)

* Docker Desktop (მოიცავს Docker Engine-სა და Docker Compose-ს) (includes Docker Engine and Docker Compose)
* Git

### ინსტალაცია (Installation)

1.  **რეპოზიტორიის კლონირება:** (Clone the repository:)

    ```bash
    # თუ ჯერ არ გაგიკეთებიათ, შექმენით ფოლდერი და გადადით მასში (If you haven't already, create a folder and navigate into it)
    # mkdir book_exchange_api
    # cd book_exchange_api
    
    # ეს ბრძანება საჭიროა მხოლოდ თუ თქვენ რეპოზიტორიიდან კლონირებთ.
    # ვინაიდან ჩვენ ვაშენებთ ნულიდან, ეს ნაბიჯი ამ ეტაპზე გამოტოვებულია.
    # (This command is only needed if you are cloning from a repository.
    # Since we are building from scratch, this step is skipped for now.)
    ```

2.  **აშენება და გაშვება Docker Compose-ის გამოყენებით:** (Build and run with Docker Compose:)

    ```bash
    docker-compose up --build
    ```
    ეს ბრძანება: (This command will:)
    * აშენებს `web` სერვისის Docker სურათს `Dockerfile`-ის საფუძველზე. (Build the `web` service Docker image based on the `Dockerfile`.)
    * გაუშვებს `db` (PostgreSQL) სერვისს. (Start the `db` (PostgreSQL) service.)
    * გაუშვებს Django-ს მიგრაციებს მონაცემთა ბაზის სქემის დასაყენებლად. (Run Django migrations to set up the database schema.)
    * გაუშვებს Django-ს განვითარების სერვერს. (Start the Django development server.)

3.  **API-ზე წვდომა:** (Access the API:)

    API იმუშავებს `http://localhost:8000`-ზე. (The API will be running on `http://localhost:8000`.)

    * **Swagger UI (API დოკუმენტაცია):** `http://localhost:8000/swagger/` (API Documentation)
    * **Redoc (ალტერნატიული დოკუმენტაცია):** `http://localhost:8000/redoc/` (Alternative Documentation)

4.  **სუპერმომხმარებლის შექმნა (Django Admin-ისთვის):** (Create a Superuser (for Django Admin):)
    გახსენით ახალი ტერმინალი `book_exchange_api` დირექტორიაში და გაუშვით: (Open a new terminal in the `book_exchange_api` directory and run:)

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    მიჰყევით მითითებებს თქვენი სუპერმომხმარებლის შესაქმნელად. შემდეგ შეგიძლიათ შეხვიდეთ Django Admin-ში `http://localhost:8000/admin/`-ზე. (Follow the prompts to create your superuser. You can then access the Django Admin at `http://localhost:8000/admin/`.)

### საწყისი მონაცემები (სურვილისამებრ) (Initial Data (Optional))

შეგიძლიათ შექმნათ საწყისი ავტორები, ჟანრები და მდგომარეობები Django Admin-ის მეშვეობით ან API ენდპოინტების გამოყენებით. (You can create some initial Authors, Genres, and Conditions through the Django Admin or by using the API endpoints.)

## API ენდპოინტები (API Endpoints)

ყველა API ენდპოინტი იწყება `/api/`-ით. დეტალური დოკუმენტაციისთვის იხილეთ Swagger UI. (All API endpoints are prefixed with `/api/`. Refer to the Swagger UI for the most up-to-date and detailed documentation.)

### მომხმარებლები (Users)

* `POST /api/register/` - ახალი მომხმარებლის რეგისტრაცია. (Register a new user.)
* `POST /api/login/` - შესვლა და აუთენტიფიკაციის ტოკენის მიღება. (Log in and get an authentication token.)
* `POST /api/logout/` - გამოსვლა (ტოკენის გაუქმება). (Log out (invalidates token).)
* `GET /api/profile/` - შესული მომხმარებლის პროფილის მიღება. (Get logged-in user's profile.)
* `PUT /api/profile/` - შესული მომხმარებლის პროფილის განახლება. (Update logged-in user's profile.)

### წიგნები (Books)

* `GET /api/books/` - ყველა ხელმისაწვდომი წიგნის სია (საჯაროდ ხელმისაწვდომია). (List all available books (publicly accessible).)
* `POST /api/books/` - ახალი წიგნის ჩამონათვალის შექმნა (მხოლოდ ავტორიზებული მომხმარებლებისთვის). (Create a new book listing (authenticated users only).)
* `GET /api/books/{id}/` - კონკრეტული წიგნის დეტალების მიღება. (Retrieve details of a specific book.)
* `PUT /api/books/{id}/` - წიგნის ჩამონათვალის განახლება (მხოლოდ მფლობელისთვის). (Update a book listing (owner only).)
* `DELETE /api/books/{id}/` - წიგნის ჩამონათვალის წაშლა (მხოლოდ მფლობელისთვის). (Delete a book listing (owner only).)
* `POST /api/books/{id}/express_interest/` - წიგნით ინტერესის გამოხატვა (ავტორიზებული მომხმარებლები). (Express interest in a book (authenticated users).)
* `GET /api/books/{id}/requests/` - კონკრეტული წიგნის ინტერესის მოთხოვნების ნახვა (მხოლოდ მფლობელისთვის). (View interest requests for a specific book (owner only).)
* `POST /api/books/{book_id}/requests/{request_id}/accept/` - წიგნის მოთხოვნის მიღება (მხოლოდ მფლობელისთვის). (Accept a book request (owner only).)
* `POST /api/books/{book_id}/requests/{request_id}/reject/` - წიგნის მოთხოვნის უარყოფა (მხოლოდ მფლობელისთვის). (Reject a book request (owner only).)

**გამოყენების შენიშვნა:**

მოთხოვნის ბილიკებში `{book_id}` და `{request_id}` წარმოადგენენ **უნიკალურ რიცხვით იდენტიფიკატორებს**:

* `{book_id}`: კონკრეტული წიგნის ID (იდენტიფიკატორი).
* `{request_id}`: ამ წიგნთან დაკავშირებული კონკრეტული მოთხოვნის ID (იდენტიფიკატორი).

**მაგალითი:**

წიგნის მოთხოვნის მისაღებად, რომლის წიგნის ID არის `10`, ხოლო თავად მოთხოვნის ID არის `5`, გამოიყენეთ შემდეგი ენდპოინტი:

`POST /api/books/10/requests/5/accept/`

### დამხმარე რესურსები (Supporting Resources)

* `GET /api/authors/`, `POST /api/authors/`, და ა.შ. (ავტორების CRUD) (CRUD for authors)
* `GET /api/genres/`, `POST /api/genres/`, და ა.შ. (ჟანრების CRUD) (CRUD for genres)
* `GET /api/conditions/`, `POST /api/conditions/`, და ა.შ. (მდგომარეობების CRUD) (CRUD for conditions)

## ტესტების გაშვება (Running Tests)

ტესტების გასაშვებად: (To run the unit tests:)

```bash
docker-compose exec web python manage.py test