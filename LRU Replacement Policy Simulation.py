# -*- coding: utf-8 -*-
"""
Created on Fri May 28 16:43:35 2021

@author: ad
"""

page_list = [] #페이지 request 리스트 ['page_num','approximate_time']
page_queue = [] #대기큐
MM=[] #프레임 
t = 0 #가상의 현재 시간

Fault = 0

#파일 read
file = input("읽을 파일을 입력: ")
f = open(f"./example_page/{file}.txt",'r')
lines = f.readlines()
f.close()

#page 추출
for line in lines:
    line = line.replace('\n','')
    line = int(line)
    line = [line, -1]
    page_list.append(line)

#Frame 개수 추출
frame_num=page_list.pop(0)
frame_num=int(frame_num[0])

#page 개수 추출
page_num = page_list.pop(0)
page_num = int(page_num[0])



def in_MM(page):
    global frame_num
    
    for i in range(len(MM)):
        if page[0] == MM[i][0]:
            return i
    return -1

def in_queue(page):
    global frame_num
    
    for i in range(len(page_queue)):
        if page[0] == page_queue[i][0]:
            return i
    return -1

    
for _ in range(page_num):
    
    #현재 request한 페이지
    page = page_list.pop(0) #['page_num','state_time']
    
    #print(page)
    
    if len(MM) < frame_num: #Frame에 자리가 있을 때
        #MM에 페이지 유무 검사
        page_in_MM = in_MM(page)
        
        if page_in_MM != -1:
            MM[page_in_MM][1] = t
            print(f'[{t}] Page request {page[0]} --> Hit')
        else:
            print(f'[{t}] Page request {page[0]} --> Initial filling')
            page[1] = t
            MM.append(page)
        
        
    
    else: #Frame이 꽉 찼을 때
        #MM에 페이지 유무 검사
        page_in_MM = in_MM(page)
        

        if page_in_MM != -1:
            MM[page_in_MM][1] = t
            print(f'[{t}] Page request {page[0]} --> Hit')
        else:
            #queue에 페이지 유무 검사
            page_in_queue = in_queue(page)
        
            old_page_index = 0 #가장 오랜 동안 참조되지 않은 페이지프레임
            for i in range(1, frame_num):
                if MM[old_page_index][1] > MM[i][1] :
                    old_page_index = i
            
            Fault += 1
            print(f'[{t}] Page request {page[0]} --> Fault ({Fault})')
            old_page = MM.pop(old_page_index)
            page_queue.append(old_page) #가장 오랜 동안 참조되지 않은  페이지프레임 큐의 맨 뒤에 추가 (내리기)
             
            #대기큐에 있는 페이지 올리기
            if page_in_queue != -1:
                pop_page = page_queue.pop(page_in_queue)
                pop_page[1] = t
                MM.append(pop_page)
                
            #MM에도 없고 대기큐에도 없는 경우 (새로운 페이지)
            else:
                page[1] = t
                MM.append(page)
            
            
    #시간 증가
    t = t+1
    
    
    #print(MM)
    #print(page_queue)
    #print()    


print()

Hit_ratio = (page_num-Fault)/page_num
print(f'Hit ratio =  {round(Hit_ratio,2)}({page_num-Fault}/{page_num})')