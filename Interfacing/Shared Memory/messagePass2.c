#include <sys/shm.h>

#include <stdio.h>

#define SHM_KEY 1656
#define SHM_SIZE sizeof(int)

int main(){
    int shm_id, *shm_value;
    key_t key = SHM_KEY;
    char *answer;

    if((shm_id = shmget(key,  SHM_SIZE, 0600)) < 0){
        perror("Shmget");
        return 1;
    }

    if((shm_value = shmat(shm_id, NULL, SHM_RDONLY)) == NULL){
        perror("Shmat");
        return 1;
    }

    if((*shm_value % 2) == 0)
        answer = "even";
    else
        answer = "odd";

    printf("The value %d is %s\n", *shm_value, answer);

    if(shmctl(shm_id, IPC_RMID, NULL) < 0){
        perror("shmctl");
        return 1;
    }

    return 0;
}
