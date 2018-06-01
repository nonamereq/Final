#include <sys/shm.h>

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SHM_KEY 1656
#define SHM_SIZE sizeof(int)

int main(){
    int shm_id, *shm_value;
    key_t key = SHM_KEY;

    srand(time(NULL));

    if((shm_id = shmget(key,  SHM_SIZE, IPC_CREAT|0600)) < 0){
        perror("Shmget");
        return 1;
    }

    if((shm_value = shmat(shm_id, NULL, 0)) == NULL){
        perror("Shmat");
        return 1;
    }

    *shm_value = (rand() % 10);

    return 0;
}
