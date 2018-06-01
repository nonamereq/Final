#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#include <stdio.h>

int main(){
    int parent_to_child[2];
    int child_to_parent[2];

    pipe(parent_to_child);
    pipe(child_to_parent);


    pid_t child;

    if((child = fork()) == 0){
        close(parent_to_child[1]);
        close(child_to_parent[0]);

        char message[100];
        read(parent_to_child[0], message, 100);
        printf("%s\n", message);
        char* message2 = "Message from child";
        write(child_to_parent[1], message2, strlen(message2));

        close(parent_to_child[0]);
        close(child_to_parent[1]);
    }else{
        close(parent_to_child[0]);
        close(child_to_parent[1]);

        char* message2 = "Message from parent";
        write(parent_to_child[1], message2, strlen(message2));
        char message[100];
        read(child_to_parent[0], message, 100);
        printf("%s\n", message);

        close(parent_to_child[1]);
        close(child_to_parent[0]);
    }
    return 0;
}
