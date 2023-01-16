import pandas as pd
import numpy as np
import random
import time
import logging
from supermarket_map import SupermarketMap
import cv2
import imageio
import glob

from customer import Customer

class Supermarket:
    """
    This is a Simulator class
    """
    def __init__(self, start_time, running_time, probs, new_mean, new_stddev, location_dic, market_layout, canvas):
        """
        Class constructor
        """
        self.cus_list = []
        self.new_cus_id = 0
        self.current_time = start_time
        self.running_time = running_time
        self.probs = probs
        self.state_list = list(probs.keys())
        self.new_mean = new_mean
        self.new_stddev = new_stddev
        self.df_doc = pd.DataFrame(columns=['timestamp','customer_no','location'])

        # for ploting
        self.location_dic = location_dic
        self.canvas = canvas
        self.market_layout = market_layout

        # statics
        self.new_customers = 0
        self.total_customers = 0
    
    def __repr__(self):
        """
        Class representation
        """
        return f'Simulation of Supermarket running for {self.running_time} minutes from {self.current_time}'

    def write_doc(self):
        """go through customer_list and write to the database 
        """
        for cus in self.cus_list:
            new_doc = pd.Series({'timestamp':self.current_time.strftime("%Y-%m-%d %H:%M:%S"), 'customer_no':cus.id, 'location':cus.state})
            self.df_doc = pd.concat([self.df_doc, new_doc.to_frame().T], ignore_index=True)
    
    def new_customer_amount(self):
        """return random integer according to the new customer rate of supermarket
        """
        new_cus = int(np.random.normal(self.new_mean,self.new_stddev))
        if new_cus < 0:
            return 0
        else:
            return new_cus

    def init_customers(self):
        """initialize customer_list according init_rate of supermarket
           and write to records to doc 
        """
        new_cus = self.new_customer_amount()
        while(new_cus == 0):
            new_cus = self.new_customer_amount()
        self.add_customers(new_cus)
        self.write_doc()
    
    def update_customers(self):
        """update current time customer state and every minute
           add new customers
           write to dataframe
           remove customers when state is checkout
        """
        self.current_time += pd.DateOffset(minutes=1)
        for cus in self.cus_list:
            cus.update_state(self.probs)
            cus.move_to(cus.state)
        new_cus = self.new_customer_amount()
        self.add_customers(new_cus)
        self.write_doc()
        
    def add_customers(self, new_cus_amount):
        """add a amount of customers and write to write to dataframe
        """
        self.new_customers = new_cus_amount
        self.total_customers += new_cus_amount
        for i in range(new_cus_amount):
            self.new_cus_id += 1
            cus = Customer(self.new_cus_id, self.location_dic)
            self.cus_list.append(cus)
   
    def remove_customers(self):
        """remove customer when state is checkout
           before remove write the doc
        """
        for cus in self.cus_list:
            if cus.state == "checkout":
                self.cus_list.remove(cus)

    def update_customer_pos(self):
        """update customer position x, y according to state
        """
        for cus in self.cus_list:
            cus.move_to(cus.state)

    def draw_customers(self):
        """draw customers to canvas
        """
        for cus in self.cus_list:
            cus.draw(self.canvas)

    def draw_text(self ,x ,y, text):
        """draw single line text, config text
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (x, y)
        fontScale = 0.5
        color = (255, 255, 255)
        thickness = 1
        image = cv2.putText(self.canvas, text, position, font, fontScale, color, thickness, cv2.LINE_AA)
        return image

    def draw_info(self):
        """draw information text
        """
        self.draw_text(32,500,self.current_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.draw_text(260,500,f'{self.new_customers} new customers coming')
        self.draw_text(260,530,f'currently {len(self.cus_list)} customers in the supermarket')
        self.draw_text(260,560,f'in total {self.total_customers} customers')

    def run_simulation(self):
        """run through the running time
           plot to canvas
           save doc to csv file
        """
        market_plan = SupermarketMap(self.market_layout)
        market_plan.draw(self.canvas)
        self.init_customers()
        self.draw_customers()
        self.draw_info()
        cv2.imshow("Supermarket simulation", self.canvas)
        min = 0
                
        while min in range(self.running_time):
            min += 1 
            time.sleep(3)

            market_plan.draw(self.canvas)
            self.update_customers()
            self.draw_customers()
            self.draw_info()
            self.remove_customers()

            # https://www.ascii-code.com/
            key = cv2.waitKey(1)
            if key == 113: # 'q' key
                break
            
            cv2.imshow("Supermarket simulation", self.canvas)
            cv2.imwrite(f'images/simu-{min}.jpg', self.canvas)

   
            
        self.df_doc.to_csv('simulation_result.csv', sep=';',index=False)
        market_plan.write_image("supermarket.png")
        time.sleep(5)
        k = cv2.waitKey(0)
        print("ASCII value of pressed key:", k)
        cv2.destroyAllWindows()
        
        image_lst = [cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB) for file in glob.glob('images/*.jpg')]
        imageio.mimsave('simu.gif', image_lst, fps=1)
        
    
        

        



    
    



    