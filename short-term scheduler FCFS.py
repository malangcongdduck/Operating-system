# -*- coding: utf-8 -*-
"""
Created on Thu May 13 16:45:33 2021

@author: ad
"""

from collections import deque

process_list = [] #['id','arrival time','service time','state', 'waiting time'] 프로세스 리스트
process_queue = deque()
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
    process_list.append(line)

#process 갯수 추출
process_num = process_list.pop(0)
process_num = int(process_num[0])

#print(process_num)
#print(process_list)

#Start
cpu_state = [] #['id', 'Turnaround Time', 'Waiting Time', 'Response Time', 'Running Time']

#CPU 점유율
cpu_utilization = 0
for process in process_list:
    cpu_utilization += process[2]
    
    
while(True):
    
    #현재 cpu가 처리중인 process의 cpu time이 전부 처리되었는지 확인하여 처리 완료 시킴
    if cpu_state: #cpu가 Idle 상태가 아닐 때
        if cpu_state[4] == Running_cpu[2]: #cpu Running Time == service time
            #종료 process 출력
            Running_cpu[3]="Exit"
            print(f'[{t}] PID({Running_cpu[0]}): {Running_cpu[3]}') #[t=exit time] PID([id]): [state]
            
            #Log 기록 계산
            cpu_state[1] = t - Running_cpu[1] #Turnaround_Time
            end_process.append(cpu_state) #Log 리스트에 넣음

            cpu_state=[] #초기화

    #더이상 프로세스 리스트에 프로세스가 없으면 종료
    if not process_list and process_num == len(end_process):
        break
    
    #process 중 arrival time이 현재시간인 process를 queue에 집어 넣는다.
    for i in range(0, len(process_list)):
        process = process_list[i]
        if process[1] == t:
            print(f'[{t}] PID({process[0]}): {process[3]}') #[t=arrived Time] PID([id]): [state] => Not-Running 출력
            process_queue.append(process_list.pop(i)) #queue에 넣음
            break
        
        
    if not cpu_state and process_queue: #cpu가 Idle 상태
        Running_cpu=process_queue.popleft()
        
        #현재 cpu 상태 업데이트
        cpu_state = [Running_cpu[0], 0, Running_cpu[4], t - Running_cpu[1], 1] #id, Turnaround Time, Waiting Time, Response Time, Running Time
        Running_cpu[3]='Running'
        #현재 process 상태 출력
        print(f'[{t}] PID({Running_cpu[0]}): {Running_cpu[3]}') #[t=Running time] PID([id]): [state]
        
    elif cpu_state:
        cpu_state[4] += 1
        

    
    #시간 t를 1만큼 증가
    t += 1 

    
    #queue에 머무는 process의 waiting time를 1만큼 증가
    for waiting_process in process_queue:
        waiting_process[4] += 1 


print()

#CPU 점유율 계산
cpu_utilization /= t
cpu_utilization *= 100

#각 프로세스별 Log 기록 출력
print('Log of Process Scheduling')
average_t = 0 #Average Turnaround Time
average_w = 0 #Average Waiting Time
average_r = 0 #Average Response Time

end_process.sort(key=lambda x: x[0]) #process id 기준으로 정렬

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