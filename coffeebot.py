#!/usr/bin/python2.7
import socket
import random

from collections import Counter
# Some basic variables used to configure the bot
server = "irc.freenode.net" # Server
port = 6667
channel = "#zuloo" # Channel
botnick = "coffeebot9000" # Your bots nick

order = {};

# This is our first function! It will respond to server Pings.
def ping():
  ircsock.send("PONG :pingis\n")

# This is the send message function, it simply sends messages to the channel.
def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

# This function is used to join channels.
def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

# This function responds to a user that inputs "Hello Mybot"
def hello():
  ircsock.send("PRIVMSG "+ channel +" :Ready to take your orders!\n")


def commands(message):
  global order
  nick=message.split('!')[0][1:]
  channel=message.split(' PRIVMSG ')[-1].split(' :')[0]
  if ircmsg.find('!order')!=-1:
    order[nick] = message.split('!order ')[-1]
  elif ircmsg.find('!reset')!=-1:
    order = {}
    hello()
  elif ircmsg.find('!bill')!=-1:
    drinks = Counter()
    empty = True
    for v in order.values():
      empty = False
      drinks[v]+=1
    sendmsg(channel,"{nick}: The order:".format(nick=nick))
    if empty:
        sendmsg(channel,"  No drinks ordered!")
    for k in drinks:
      sendmsg(channel,"  {value} {key}".format(key=k, value=str(drinks[k]).rjust(3)))
  elif ircmsg.find('!whoshouldpay')!=-1:
      paylist = ['Kristian', 'Armin', 'Ed', 'Jan', 'Thomas', 'Bernd', 'Christian',
                 'Nobody is allowed coffee today. Sorry. Back to work!']
      sendmsg(channel,random.choice(paylist))
  elif ircmsg.find('!suggest')!=-1:
      drinklist = ['LATTE MACCIATTOOO!', 'Espresso', 'Double Espresso', 'Café',
                   'Cappucino', 'Hot Chocolate day!',
                   'LLAAAATTEE MAAAAACCCCCCIIIIIAAAATTTTOOOOOO!!!1!!!1!!one!!1',
                   'I think you should go thirsty today.', 'Quadruple Espresso']
      sendmsg(channel,random.choice(drinklist))
  elif ircmsg.find('!xig')!=-1:
      xiglist = ['b', 'd', 'f', 'g', 'j', 'l', 'm', 'n',
        'r', 's', 't', 'w', 'z', 'br', 'bl', 'p',
        'dr', 'fl', 'fr', 'gl', 'gr', 'pl', 'pr',
        'sn', 'sp', 'st', 'sw', 'tr', 'tw', 'wr',
        'ch', 'cl', 'kl', 'kr', 'schw', 'sch',
        'schl', 'y']
      c1 = random.choice(xiglist)
      c2 = random.choice(xiglist)
      while c2 == c1:
          c2 = random.choice(xiglist)
      sendmsg(channel, c1.title()+'iggly'+c2+'uff?')
  elif ircmsg.find(botnick+":")!=-1 or ircmsg.find("!help")!=-1:
    sendmsg(channel, "!order drink - order the drink")
    sendmsg(channel, "!bill - show the summed orders")
    sendmsg(channel, "!reset - reset the orders")
    sendmsg(channel, "!whoshouldpay - decides who should pay")
    sendmsg(channel, "!suggest - tells indecisive people what to drink")
    sendmsg(channel, "!xig - generates a random Xigglyxuff! :D")
# Here we connect to the server using the port 6667
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, port))
# user authentication
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :coffeebot\n")
# here we actually assign the nick to the bot
ircsock.send("NICK "+ botnick +"\n")

# Join the channel using the functions we previously defined
joinchan(channel)

hello()

# Be careful with these! it might send you to an infinite loop
while 1:
  # receive data from the server
  ircmsg = ircsock.recv(2048)
  # removing any unnecessary linebreaks.
  ircmsg = ircmsg.strip('\n\r')
  # Here we print what's coming from the server
  #print(ircmsg)
  if ircmsg.find(' PRIVMSG ')!=-1:
    commands(ircmsg)

  # if the server pings us then we've got to respond!
  if ircmsg.find("PING :") != -1:
    ping()
