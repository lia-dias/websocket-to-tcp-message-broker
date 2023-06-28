
#include <stdio.h>
#include <stdlib.h>

void readBytes(long bytes_length, unsigned char * ptr) {
    for (long i = 0; i < bytes_length; i++) {
        scanf("%u", (unsigned *) (ptr+i));
    }
}

unsigned char * getMessageContent(unsigned char * ptr, unsigned long offset, unsigned long content_length, unsigned char content_mask[4]) {
    unsigned char * decrypted_message = malloc(sizeof(unsigned char) * (content_length + 1));
    unsigned long i = 0;
    for(; i < content_length; i++) {
        decrypted_message[i] = *(ptr+offset+i) ^ content_mask[i % 4];
    }
    decrypted_message[i] = '\0';
    return decrypted_message;
}

unsigned long getMessageSize(unsigned char * ptr, unsigned long * offset) {
    if(ptr[0] - 128 <= 125) {
        *offset = 1;
        return ptr[0] - 128;
    } else if (ptr[0] == 126) {
        *offset = 3;
        readBytes(2, ptr + 1);
        return (unsigned short int) ptr[1] << 8 | ptr[2];
    } else {
        *offset = 9;
        readBytes(8, ptr + 1);
        return (unsigned long) ptr[1] << 56 | (unsigned long) ptr[2] << 48 | (unsigned long) ptr[3] << 40 | (unsigned long) ptr[4] << 32 | (unsigned long) ptr[5] << 24 | (unsigned long) ptr[6] << 16 | (unsigned long) ptr[7] << 8 | ptr[8];
    }
}

int main() {
    // initialize
    unsigned long offset = 0;
    unsigned char control_bytes[9]; 
    unsigned char *message;

    scanf("%hu", (unsigned short *) control_bytes);
    
    unsigned long content_length = getMessageSize((unsigned char *) &control_bytes, &offset);

    unsigned long message_length = content_length + 4 + offset;

    message = (unsigned char *) malloc((sizeof(unsigned char *) * message_length));
    
    readBytes(message_length, message + offset);

    // get message metadata
    unsigned char *content_mask_posix = message+offset;
    offset = offset + 4;

    //decrypt message
    unsigned char *decrypted_message = getMessageContent(message, offset, content_length, content_mask_posix);
    printf("%s\n", decrypted_message);

}