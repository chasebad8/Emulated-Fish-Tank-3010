package com.example.petthing;

import androidx.appcompat.app.AppCompatActivity;

import java.net.*;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    Button feed;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        feed = (Button) findViewById(R.id.feed);

        feed.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                DatagramSocket socket= null;

                try
                {

                    InetAddress host = InetAddress.getByName( "127.0.0.0" ) ;
                    int port = 1025;

                    socket = new DatagramSocket() ;

                    String message = "1";
                    byte [] data = message.getBytes() ;
                    DatagramPacket packet = new DatagramPacket( data, data.length, host, port ) ;
                    socket.send( packet ) ;

                }
                catch( Exception e )
                {
                    System.out.println( e ) ;
                }
                finally
                {
                    if( socket != null )
                        socket.close() ;
                }
            }
        });
    }
}
