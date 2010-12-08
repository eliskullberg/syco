#! /usr/bin/env python

import sys, ConfigParser, os, re, socket

import general
#
#  Contains global functions and settings for the fosh app
#

class Options:
  verbose=1
  
options = Options()

# The version of the fosh script
version="0.1"
parser=''

fosh_path=os.path.abspath(sys.path[0] + "/../") 
config_file_name=fosh_path + "/etc/install.cfg"
config = ConfigParser.RawConfigParser()
config.read(config_file_name)

def print_error(message):
  print_verbose(message, caption=general.BOLD + "Error: " + general.RESET)
    
def print_info(message):
  print_verbose(message, caption="Info: ") 
    
def print_verbose(message, verbose_level = 1, caption=""):
  global options

  messages = []
  if (not isinstance(message, tuple)):
    messages.append(message)
  else:
    messages = message
  
  for msg in messages:    
    host=socket.gethostname() + ": "
    if (msg):
      msg=re.sub("[\n]", "\n" + host + caption, str(msg))
    msg=host + caption + msg
  
    if (options.verbose >= verbose_level):    
      print(msg)

def get_option(section, option):
  if (config.has_section(section)):
    if (config.has_option(section, option)):
      return config.get(section, option)  
    else:      
      print_error("Can't find option '" + option + "' in section '" + section + "' in install.cfg")          
  else:
    print_error("Can't find section '" + section + "' in install.cfg")
          
def get_root_password():
  return get_option("general", "root_password")

def get_ip(host_name):
  return get_option(host_name, "server")

def get_mac(host_name):
  return get_option(host_name, "mac")

def get_ram(host_name):
  return get_option(host_name, "ram")

def get_cpu(host_name):
  return get_option(host_name, "cpu")

def get_servers():
  global config
  servers=config.sections()
  servers.remove("general")
  return servers
  
def get_commands(host_name):
  options = []
  
  if (config.has_section(host_name)):
    for option, value in config.items(host_name):
      option=option.lower()
      if "command" in option:
        options.append([option, value])

  return sorted(options)
  
def get_guests(host_name):
  guests = []
  
  if (config.has_section(host_name)):
    for option, value in config.items(host_name):
      if ("guest" in option):
        guests.append(value)

  return sorted(guests)  