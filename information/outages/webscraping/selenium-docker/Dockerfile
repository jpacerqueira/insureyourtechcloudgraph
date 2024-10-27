FROM python:3.12-bookworm

RUN apt-get update 
RUN apt-get install -y tar gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

#download and install chrome
# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN google-chrome --version

#download and install mozilla driver
#RUN cd /tmp/ ; wget -O geckodriver.tar.gz  "https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux-aarch64.tar.gz" ; tar -xvzf /tmp/geckodriver.tar.gz  -C /opt/ ; chmod 755 /opt/geckodriver ; ln -fs /opt/geckodriver /usr/bin/geckodriver ; ln -fs /opt/geckodriver /usr/local/bin/geckodriver 
#RUN whereis geckodriver
#RUN echo 'export PATH=$PATH:/usr/bin/geckodriver' >> ~/.bash_profile ; source ~/.bash_profile ; geckodriver --version


#install python dependencies
COPY requirements.txt requirements.txt 
RUN pip install -r ./requirements.txt 


#some envs
ENV APP_HOME /app 
ENV PORT 5000

#set workspace
WORKDIR ${APP_HOME}

#copy local files
COPY . . 

CMD exec gunicorn --bind :${PORT} --workers 1  main:app # main:app
