# -*- coding: utf-8 -*-
"""
Created on Thu May 13 21:37:12 2021

@author: ad
"""




process_list = [] #['id','arrival time','service time','state', 'waiting time'] 프로세스 리스트
process_queue = []
process_num = 0 #프로세스 개수
t = 0 #가상의 현재 시간
end_process = [] #Log of Process Scheduling 출력에 사용할 프로세스들의 Log 리스트

#파일 read
file = input("읽을 파일을 입력: ")
f = open(f"./example_fcfs_srt/{file}.txt",'r')
lines = f.readlines()
f.close()

#process 추출
for line in lines:
    line = line.split(" ")
    line = ' '.join(line).split()
    line = list(map(int,line))
    line.append('Not-Running')
    line.append(0) #waiting time
    line.append(-1) #처음 cpu 점유 시간 -1이면 한번도 실행되지 않은 상태
    process_list.append(line)

#process 갯수 추출
process_num = process_list.pop(0)
process_num = int(process_num[0])

#print(process_num)
#print(process_list)

#Start
cpu_state = [] #['id', 'Turnaround Time', 'Waiting Time', 'Response Time', 'Running Time', Service Time-Running Time]
#flag=0 어떤 if문이 실행되는지 확인하기 위한 flag

#CPU 점유율
cpu_utilization = 0
for process in process_list:
    cpu_utilization += process[2]
    
while(True):
    
    #현재 cpu가 처리중인 process의 cpu time이 전부 처리되었는지 확인하여 처리 완료 시킴
    if cpu_state: #cpu가 Idle 상태가 아닐 때
        if cpu_state[4] == 0: #cpu Service Time-Running Time == 0
            #종료 process 출력
            Running_cpu[3]="Exit"
            #print(f'[{t}] PID({Running_cpu[0]}): {Running_cpu[3]}') #[t=exit time] PID([id]): [state] //기존 FCFS 과제 출력 형태
            
            #Log 기록 계산
            cpu_state[1] = t - Running_cpu[1] #Turnaround_Time
            cpu_state[3] = Running_cpu[5] - Running_cpu[1] #Response Time
            end_process.append(cpu_state) #Log 리스트에 넣음

            cpu_state=[] #초기화
            
    #더이상 프로세스 리스트에 프로세스가 없으면 종료
    if not process_list and process_num == len(end_process):
        break
        
    #process 중 arrival time이 현재시간인 process를 queue에 집어 넣는다. ************
    for i in range(0, len(process_list)):
        process = process_list[i]
        if process[1] == t:
            #print(f'[{t}] PID({process[0]}): {process[3]}') #[t=arrived Time] PID([id]): [state] => Not-Running 출력  //기존 FCFS 과제 출력 형태
            process_queue.append(process_list.pop(i)) #queue에 넣음
            break
        
        
    if not cpu_state and process_queue: #cpu가 Idle 상태 (큐가 비어있지 않음) (1)
        #예상되는 남아있는 실행 시간이 가장 짧은 프로세스 선택 
        remain_min_process = 0
        for i in range(1, len(process_queue)):
            if process_queue[i][2] < process_queue[remain_min_process][2]:
                remain_min_process = i
        
        Running_cpu = process_queue.pop(remain_min_process)
        
        #현재 cpu 상태 업데이트 (실행)
        Running_cpu[3] = 'Running'
        Running_cpu[2] -= 1
        
        #Response Time을 계산하기 위해 처음 실행된 프로세스와 다시 실행된 프로세스 구분
        if Running_cpu[5] == -1:
            Running_cpu[5] = t
            
        cpu_state = [Running_cpu[0], 0, Running_cpu[4], Running_cpu[5], Running_cpu[2]] #id, Turnaround Time, Waiting Time, Response Time, Service Time-Running Time
        
        #현재 process 상태 출력
        #print(f'[{t}] PID({Running_cpu[0]}): {Running_cpu[3]}') #[t=Running time] PID([id]): [state]  //기존 FCFS 과제 출력 형태
        #flag=1
        
        
    elif cpu_state and process_queue: #cpu가 Idle 상태가 아닐 때 (큐가 비어있지 않음) (2)
        #queue에서 남은 실행 시간 짧은 프로세스 검색
        remain_min_process = 0
        for i in range(1, len(process_queue)):
            if process_queue[i][2] < process_queue[remain_min_process][2]:
                remain_min_process = i
        
        #queue에 있는 실행 시간이 가장 짧은 프로세스와 현재 프로세스의 남은 실행 시간 비교**************
        if cpu_state[4] > process_queue[remain_min_process][2]: #큐의 프로세스가 더 짧을 때
            Running_cpu[3] = 'Wait'
            temp = Running_cpu #임시 저장
            Running_cpu = process_queue.pop(remain_min_process) #짧은 프로세스 선택
            Running_cpu[3] = 'Running'
            process_queue.insert(0, temp) #다시 큐에 넣음
            
            #Response Time을 계산하기 위해 처음 실행된 프로세스와 다시 실행된 프로세스 구분
            if Running_cpu[5] == -1:
                Running_cpu[5] = t
            
            cpu_state = [Running_cpu[0], 0, Running_cpu[4], Running_cpu[5], Running_cpu[2]] #id, Turnaround Time, Waiting Time, Response Time, Service Time-Running Time
            
            #프로세스 전환 후 실행
            cpu_state[4] -= 1
            Running_cpu[2] -= 1
            
            #현재 process 상태 출력
            #print(f'[{t}] PID({Running_cpu[0]}): {Running_cpu[3]}') #[t=Running time] PID([id]): [state]  //기존 FCFS 과제 출력 형태
            #flag=2
            
        else: #cpu가 점유한 프로세스가 더 짧을 때 (3)
            cpu_state[4] -= 1
            Running_cpu[2] -= 1
            #flag=3
            #print(f'[{t}] PID({Running_cpu[0]}): {Running_cpu[3]} Responsetime: {Running_cpu[5]}') #[t=Running time] PID([id]): [state]
            
    elif cpu_state and not process_queue: #cpu가 Idle 상태가 아니고 queue가 비었을 때 (4)
        cpu_state[4] -= 1
        Running_cpu[2] -= 1
        #flag=4
        #print(f'[{t}] PID({Running_cpu[0]}): {Running_cpu[3]} Responsetime: {Running_cpu[5]}') #[t=Running time] PID([id]): [state]
    
    else: #cpu가 Idle 상태이고, queue가 비었을 때 (5)
        if process_num == len(end_process): #다음에 올 프로세스가 더이상 없을 때 종료
            pass
            #flag=5

    
    '''
    #확인 출력
    print(f'\nflag({flag})*********id:{Running_cpu[0]}************ time:{t}')
    print(Running_cpu)
    print(cpu_state)

    print()
    '''

    #시간 t를 1만큼 증가
    t += 1 
    
    #queue에 머무는 process의 waiting time를 1만큼 증가
    for waiting_process in process_queue:
        waiting_process[4] += 1 


    
print()

#CPU 점유율 계산
cpu_utilization /= t
cpu_utilization *= 100


#각 프로세스별 Log 기록 출력 형태
print('Log of Process Scheduling')
average_t = 0 #Average Turnaround Time
average_w = 0 #Average Waiting Time
average_r = 0 #Average Response Time


end_process.sort(key=lambda x: x[0]) #process id 기준으로 정렬

#기존의 FCFS 과제 출력
for Log in end_process:
    average_t += Log[1]
    average_w += Log[2]
    average_r += Log[3]

    print(f'PID({Log[0]})    Turnaround Time: {Log[1]}    Waiting Time : {Log[2]}    Response Time : {Log[3]}')
    
    
print()


print(f'Average Turnaround Time: {round(average_t/process_num, 2)}')
print(f'Average Waiting Time: {round(average_w/process_num, 2)}')
print(f'Average Response Time: {round(average_r/process_num, 2)}')
print(f'CPU Utilization        : {round(cpu_utilization, 2)}%')
