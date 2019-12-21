
// Server side implementation of UDP client-server model 
#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 

#include <errno.h>
#include <fcntl.h> 
#include <termios.h>

#include "broad.h"
  
#define PORT    9123 
#define MAXLINE 1024
char *portname = "/dev/ttyO3";
//char *portname = "/dev/ttyUSB0";

#define error_message printf

// Driver code 
int main() { 
    int sockfd; 
    char buffer[MAXLINE]; 
    char *hello = "Hello from server"; 
    struct sockaddr_in servaddr, cliaddr; 

    printf("starting server...");
      
    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket creation failed"); 
        exit(EXIT_FAILURE); 
    } 
      
    memset(&servaddr, 0, sizeof(servaddr)); 
    memset(&cliaddr, 0, sizeof(cliaddr)); 
      
    // Filling server information 
    servaddr.sin_family    = AF_INET; // IPv4 
    servaddr.sin_addr.s_addr = INADDR_ANY; 
    servaddr.sin_port = htons(PORT); 
      
    // Bind the socket with the server address 
    if ( bind(sockfd, (const struct sockaddr *)&servaddr,  
            sizeof(servaddr)) < 0 ) 
    { 
        perror("bind failed"); 
        exit(EXIT_FAILURE); 
    } 
      
    int n; 
    unsigned int len;
    n = recvfrom(sockfd, (char *)buffer, MAXLINE,  
                MSG_WAITALL, ( struct sockaddr *) &cliaddr, 
                &len); 
    n = recvfrom(sockfd, (char *)buffer, MAXLINE,               //BUG? or is it fundamental? (for 32bit only)
                MSG_WAITALL, ( struct sockaddr *) &cliaddr, 
                &len); 
    buffer[n] = '\0'; 
    printf("Client said: %s\n", buffer); 
    /* example of message sending
    sendto(sockfd, (const char *)hello, strlen(hello),  
        MSG_CONFIRM, (const struct sockaddr *) &cliaddr, 
            len); 
    printf("Hello message sent.\n");  
    */

    int fd = open(portname, O_RDWR | O_NOCTTY | O_SYNC);
    if (fd < 0)
    {
        error_message ("error %d opening %s: %s\n", errno, portname, strerror (errno));
        return -1;
    }

    set_interface_attribs (fd, B115200, 0);  // set speed to 4800 bps, 8n1 (no parity)
    set_blocking (fd, 0);                // set blocking

    //write (fd, "hello!\n", 7);           // send 7 character greeting

    //usleep ((7 + 25) * 1090);             // sleep enough to transmit the 7 plus

    unsigned char data[5];//forward_left, forward, forward_right, doppler, zero

    n = read (fd, data, 4);  // read up to 100 characters if ready to read
    
    int shift = 0;
    int i;
    for(i =0;i<4;i++){
        if(data[i] < 2)
            shift = i;
    }
    shift = (shift +1)%4;
    //n = read(fd, data,shift);
   while(1){
        n = read (fd, data, 4);  // read up to 100 characters if ready to read
        //if(count %2 == 0)
        printf("%i, %i, %i, %i\n",data[0],data[1],data[2],data[3]);
        sendto(sockfd, (const unsigned char *)data, 4,  MSG_CONFIRM, (const struct sockaddr *) &cliaddr, len);
        //usleep (10000); 2

   }
      
    return 0; 
} 
