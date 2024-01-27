# Terra Store System Recommendation  
## Description  
Terra Store is a new unicorn candidate in Indonesia. Terra Store now has a very small market cap, but soon this startup will be a unicorn. To make their dreams come true, Terra Store wants to implement AI into their service to find out what their users want to buy in the future. Terra Store finds that AI will make their revenue go to the moon, and they think that if they implement this AI, it will go public soon. To implement this AI, Terra Store wants me to do it since I'm a new intern member in the AI Department of this startup. So I will carry this huge responsibility to create a recommendation system with AI.


In these repositories, I implement full-stack software and model development. The AI modeling process and software development are included in this repository. To create a recommendation AI model, I used the SVD method. Singular Value Decomposition is a recommendation system method that can be used to predict a value, such as a rating value, from a product that has never been bought by the user. I use SVD because it gives me low MAE and RMSE results.

This website is run under the FastAPI framework. I choose FastAPI because it's fast and can autogenerate the code API documentation using Swagger. This system will run using Docker, because I believe if the system is run on my computer, it will run on your computer. I also used PostgreSQL since this database has good performance and is free to use.

I hope this system can help the Terra Store startup win a pitch after the lunch break, since the CEO wants me to do this from morning until lunch break. Thank you!!

## Requirements
- Docker>=24.0 
- Docker Compose>=2.0
- Python >= 3.9

## How to run   
To run this system, please open and copy the `.env.example` to `.env` first. After that, please change or fill in the empty variable by using this reference.
- SQL_USER is the user that will be used by the SQL
- SQL_PASSWOWRD is the password that will be used by the SQL
- SQL_HOST is the hostname of the SQL that can be accessed from inside a web container. Since the service name that we used is "db" in the docker-compose, please use it.
- SQL_DB is the database name.
- SQL_PORT is the SQL port inside the container that can be accessed by the web container.
- SQL_PORT_OUT is the SQL port outside the container that can be accessed by the public.
- TIME_ZONE is the time Zone is the default timezone of the system.
- WEB_PORT is the port of the web inside the container.
- WEB_PORT_OUT is the port of the web that can be accessed by the public.

```
git clone https://github.com/m4ri01/terra-store-recommendation-system.git
cd terra-store-recommendation-system
docker-compose up -d 
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements/local.txt #install library for seeding data
python3 seed.py # Seed the default data to website
```

To open the website, you can open `http://YOUR_LOCAL_OR_PUBLIC_IP_ADDRESS:WEB_PORT_OUT`. Please check the `.env.example` for the WEB_PORT_OUT.
