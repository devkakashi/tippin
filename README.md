# WHAT IS THE PROJECT?

The project aims to implement the tippin.me service on its linux terminal.

# CONFIGURING THE ENVIRONMENT

```bash
sudo su && apt-get update
apt-get upgrade && apt-get install python3
apt-get install python3-pip && apt-get install git
git clone https://github.com/devkakashi/tippin
cd tippin
```

##### 1 - One step :  program installation is packages

```install packages
pip3 -r requirements.txt
```

```
chmod +x tippin.py
mv tippin.py tippin && cp tippin /usr/bin
exit
```


##### 2 - First step: Add twitter credentials to tippin.

###### CTRL + ALT + T
```
tippin -u username -p password
```

# What is possible to do with the software?

#### .1 You can generate very fast payment invoices it's easy.

```
tippin --newinvoice amount
```
![Screenshot](https://i.imgur.com/4uI7vXk.png)

#### .2 You can withdraw at any time you wish.

```
tippin --cashout invoice
```
![Screenshot](https://i.imgur.com/CvARcF4.png)

### .3 You can check the status of an invoice you generated.
```
tippin --status invoice
```
![Screenshot](https://i.imgur.com/LjOEXHK.png)

Make a donation so I can buy a coffee mug is keep coding [tippin.me](https://tippin.me/@devkakashi)
#
Follow me on twitter [Twitter](https://twitter.com/devkakashi)
#
WARNING! As it is a software that is under development there may be crash bugs etc... avoid transacting large amounts as there may be a problem
