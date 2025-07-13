# socketとosモジュールをインポートします
import socket, os

# UNIXソケットをストリームモードで作成します
# I'm gonna create the UNIX socket as a stream mode
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# このサーバが接続を待つUNIXソケットのパスを設定します
# Set the path of the UNIX socket that the server will wait for connections
server_address = '/tmp/socket_file'

# 以前の接続が残っていた場合に備えて、サーバアドレスをアンリンク（削除）します
# If there is a previous connection, unlink the server address
try:
   os.unlink(server_address) 
# サーバアドレスが存在しない場合、例外を無視します
# If the server address does not exist, ignore the exception
except FileNotFoundError:
   pass

# サーバアドレスにソケットをバインド（接続）します
# Bind the socket to the server address
sock.bind(server_address)

# ソケットが接続要求を待機するようにします
# Listen for connection requests on the socket
sock.listen(1)

# 無限ループでクライアントからの接続を待ち続けます
# Wait for connections from clients in an infinite loop
while True:
    # クライアントからの接続を受け入れます
    # Accept a connection from a client
    connection, client_address = sock.accept()
    try:
        print("Connection from", client_address)

        # ループが始まります。これは、サーバが新しいデータを待ち続けるためのものです。
        # The loop starts. This is to allow the server to wait for new data
        while True:
            # ここでサーバは接続からデータを読み込みます。
            # Here the server reads data from the connection
            # 16という数字は、一度に読み込むデータの最大バイト数です。
            # 16 is the maximum number of bytes to read at once
            data = connection.recv(16)
            
            # 受け取ったデータはバイナリ形式なので、それを文字列に変換します。
            # The received data is in binary format, so we need to convert it to a string
            # 'utf-8'は文字列のエンコーディング方式です。
            # utf-8 is the encoding method for strings            
            data_str = data.encode('utf-8')

            # 受け取ったデータを表示します。
            # Display the received data
            print('Received "{}"'.format(data_str))

            # もしデータがあれば（つまりクライアントから何かメッセージが送られてきたら）以下の処理をします。
            # If there is data (i.e. if a message is sent from the client) do the following processing
            if data:
              # 受け取ったメッセージを処理します。
              # Process the received message
              response = 'Processing ' + data_str

              # 処理したメッセージをクライアントに送り返します。
              # Send the processed message to the client
              # ここでメッセージをバイナリ形式（エンコード）に戻してから送信します。
              # Here we convert the message to binary format (encode) before sending it
              connection.sendall(response.encode())

            # クライアントからデータが送られてこなければ、ループを終了します。
            # If no data is sent from the client, end the loop
            else:
                print("No data from", client_address)
                break
    finally:
       print("Closing current connection")
       connection.close()
    

                
