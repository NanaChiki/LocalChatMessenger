import socket
# sysモジュールは、Pythonが実行されているシステムに関連する情報を取得したり、
# システム特有の操作を行ったりするためのPythonの組み込みモジュールです。
# sys module is a built-in module that provides information about the system,
# and allows for system-specific operations.
import sys

# TCP/IPソケットを作成します。
# ここでソケットとは、通信を可能にするためのエンドポイントです。
# Create a TCP/IP socket
# Where the socket is an endpoint that allows communication
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# サーバが待ち受けている特定の場所にソケットを接続します。
# Connect the socket to the specific location where the server is waiting
server_address = '/tmp/socket_file'
print("Connecting to {}".format(server_address))

# サーバに接続を試みます。
# 何か問題があった場合、エラーメッセージを表示してプログラムを終了します。
# Try to connect to the server.
# If there is a problem, display an error message and exit the program
try:
  sock.connect(server_address)
except socket.error as e:
  print("Socket connection failed: {}".format(e))
  # sys.exit()を使うと、Pythonプログラムをすぐに終了することができます。
  # ここでの引数1は、プログラムがエラーで終了したことを示すステータスコードです。
  # sys.exit() allows you to exit the Python program immediately.
  # The argument 1 here is a status code that indicates that the program has ended with an error
  sys.exit(1)

# サーバに接続できたら、サーバにメッセージを送信します。
# Once the connection is established, send a message to the server
try:
  # 送信するメッセージを定義します。
  # ソケット通信ではデータをバイト形式で送る必要があります。
  # Define the message to send
  # In socket communication, data must be sent in binary format
  message = b'Sending a message to the server side'
  sock.sendall(message)

  # サーバからの応答を待つ時間を2秒間に設定します。
  # この時間が過ぎても応答がない場合、プログラムは次のステップに進みます。
  # Set the time to wait for a response from the server to 2 seconds.
  # If no response is received within this time, the program will proceed to the next step
  sock.settimeout(2)

  # サーバからの応答を待ち、応答があればそれを表示します。
  # Wait for a response from the server and display it if there is one
  try:
    while True:
      # サーバからのデータを受け取ります。
      # 受け取るデータの最大量は32バイトとします。
      # Receive data from the server
      # The maximum amount of data to receive is 32 bytes
      data = str(sock.recv(32))

      # データがあればそれを表示し、なければループを終了します。
      # Display the data if it exists, otherwise end the loop
      if data:
        print('Server response: ' + data)
      else:
        break

  # 2秒間サーバからの応答がなければ、タイムアウトエラーとなり、エラーメッセージを表示します。
  # If no response from the server for 2 seconds, a timeout error occurs and an error message is displayed
  except (TimeoutError):
    print('Socket timeout, ending listening for server messages')


# すべての操作が完了したら、最後にソケットを閉じて通信を終了します。
# Once all operations are complete, close the socket and end the communication
finally:
  print('Closing socket')
  sock.close()