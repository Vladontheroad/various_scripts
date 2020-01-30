#!/usr/bin/env python3
# Requires python 3+
import sys
import ipaddress
import re

def ErrorMessage():
    print("ERROR : input not understood. Type no argument for usage examples.")

def Usage():
    print("Usage: command.py ARGS\n")
    print("Examples of ARGS values:")
    print("'.252'\n\t Shows several potentials netmasks and related infos\n\t (255.255.255.252 and 255.255.252.0 in this case).")
    print("'/29'\n\t Shows infos related to a /29 prefix")
    print("'.10/28'\n\t Shows infos related to 10.10.10.10/28")
    print("'.33.10/22'\n\t Shows infos related to 10.10.33.10/22")
    print("'.172.48.16/20'\n\t Shows infos related to 10.172.48.16/20")
    print("'10.10.10.1 255.255.224.0'\n\t For Cisco 'show run int' output compatibility format")
    print("'10.10.10.1/22'\n\t For Cisco 'show ip int' output compatibility format")
    print("")
def FHosts(NetworkInput):
# Print hosts
# Input example : "192.168.118.1/24"
    try:
        ANetwork = ipaddress.IPv4Network(NetworkInput, False)
    except (ipaddress.AddressValueError,ipaddress.NetmaskValueError):
        ErrorMessage()
        return 1
    AHosts=list(ANetwork.hosts())
    print("Hosts: "+str(AHosts[0])+"-"+str(AHosts[len(AHosts)-1]), end="\t\t")
    print("Hosts number: "+str((ANetwork.num_addresses)-2))

def FNetmask(NetworkInput):
# Print netmask & associated wildcard mask
# Input examples: "/28" ".252"
    try:
        ANetwork = ipaddress.IPv4Network(NetworkInput, False)
    except (ipaddress.AddressValueError,ipaddress.NetmaskValueError):
        ErrorMessage()
        return 1
    AWildcard = ANetwork.hostmask
    APrefixlen = ANetwork.prefixlen
    ANetmask = ((ANetwork.with_netmask).split('/',1))[1]
    print("Nm: "+str(ANetmask)+" (/"+str(APrefixlen)+")", end="\t\t\t")
    print("Wc: "+str(AWildcard))

#def RemoveSpace(Input):
# Remove heading and trailing spaces without removing in-between spaces
# TODO : to be continued, see FUN videos to avoid memory waste
#    while(Input[0]==' '):
#        Input[0].strip()
#    while(len(Input)==' '):
#        Input[:1].strip()
#    return Input
        
def FInputAnalysis():
# Input analysis
    UserInput = str(input("Input (h for help) >> "))
    
    #TODO : uncomment and complete once RemoveSpace() is finished
    #if(len(UserInputRaw.strip(" "))>0):
    #    UserInput = RemoveSpace(UserInputRaw)
    #else:
    #    ErrorMessage()
    #    return
        
    if(UserInput[:1]=='/'):
        NetworkObject=str("10.10.10.0"+UserInput)
        Result = FNetmask(NetworkObject)
        if(Result!=1):
            FHosts(NetworkObject)
    elif(UserInput[:1]=='.'):
        # If input start with "."
        # 1 - contains only 1 "."
        if(UserInput.count(".")==1):
            if(UserInput.count("/")==0):
                NetworkObject=str("10.10.10.0/255.255.255"+UserInput)
                print("Interpreting as netmask 255.255.255"+UserInput)
                Result = FNetmask(NetworkObject)
                if(Result!=1):
                    FHosts(NetworkObject)                

                    NetworkObject=str("10.10.10.0/255.255"+UserInput+".0")
                    print("\nInterpreting as netmask 255.255"+UserInput+".0")
                    Result = FNetmask(NetworkObject)
                    if(Result!=1):
                        FHosts(NetworkObject)
                
                # /16 and less not necessary useful info
                #NetworkObject=str("10.10.10.0/255"+UserInput+".0.0")
                #print("\nInterpreting as netmask 255"+UserInput+".0.0")
                #FNetmask(NetworkObject)
                #FHosts(NetworkObject)
            else:
                NetworkObject=str("10.10.10"+UserInput)
                Result = FNetmask(NetworkObject)
                if(Result!=1):
                    FHosts(NetworkObject)
        # 2 - contains 2 ".", requires netmask and interpret as VLSM 10.10.* subnet
        elif(UserInput.count(".")==2):
            NetworkObject=str("10.10"+UserInput)
            Result = FNetmask(NetworkObject)
            if(Result!=1):
                FHosts(NetworkObject)
        # 3 - contains 3 ".", same as 2 with 10.* subnet
        elif(str(UserInput).count(".")==3):
            NetworkObject=str("10"+UserInput)
            Result = FNetmask(NetworkObject)
            if(Result!=1):
                FHosts(NetworkObject)
        else:
            print("ERROR : TODO : print usage examples")

    elif((" " in UserInput) and (len(UserInput) >= 15)):
        # Input like "0.0.0.0 0.0.0.0" or "ip netmask"
        NetworkObject=UserInput.replace(' ','/')
        print(NetworkObject)
        Result = FNetmask(NetworkObject)
        if(Result!=1):
            FHosts(NetworkObject)
        
    elif(UserInput == 'h'):
        Usage()
        
    elif(UserInput == 'q'):
        sys.exit(1)
        
    else:
        NetworkObject=UserInput
        Result = FNetmask(NetworkObject)
        if(Result!=1):
            FHosts(NetworkObject)
        

if __name__ == '__main__':
#    len_argv =(len(sys.argv)-1)
#    if((len_argv >= 1) and (len_argv <3)):
#        FInputAnalysis(str(sys.argv[1]))
#    elif(len_argv > 2):
#        ErrorMessage()
#    else:
#        Usage()
#
    while(True):
        FInputAnalysis()
