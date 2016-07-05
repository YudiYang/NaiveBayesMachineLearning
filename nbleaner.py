#!/usr/bin/python


#####################Naive Bayes Learn#####################
#Class:  USC-EE599
#Author: Yudi Yang
#USC ID: 5017708933
#Email:  yudiyang@usc.edu
#Version: 1.0
#######################################################


import os,re,sys
import collections
import numpy as np

class Learner():
	"""docstring for Classifier"""
	def __init__(self,argv):
		self.spam_total = collections.Counter()
		self.ham_total  = collections.Counter()
		self.originalTrain()
		self.dataCal()
		self.savefile(argv)

	def savefile(self,argv):
		np.savetxt(argv,self.save_list,fmt='%s',delimiter=',')

	def getCounter(self,filesource):
		'''Given a File, count all words in this file'''
		wordPattern = r'''[A-Za-z]+|\$?\d+%?$''' 		##this is the regular expression to find each word.
		fi = open(filesource)
		ri = re.findall(wordPattern,fi.read())						##get all words from the file
		return collections.Counter(ri)								##give back the result of counting words.



	def filesCounter(self,path):
		total_counter = collections.Counter()
		for file in os.listdir(path):
			if(file.endswith('.txt')):
				print '==============================\n'
				print 'DEALING WITH FILE: %s',file
				print '==============================\n'
				total_counter += self.getCounter(path+'/'+file)

		return total_counter

	def originalTrain(self):
		self.spam_size = 0
		self.ham_size = 0
		for i in range(1,5):
			path_spam = './training_data/enron'+str(i)+'/spam'
			path_ham = './training_data/enron'+str(i)+'/ham'
			self.spam_size += len(os.listdir(path_spam))
			self.ham_size += len(os.listdir(path_ham))
			self.spam_total+=self.filesCounter(path_spam)
			self.ham_total +=self.filesCounter(path_ham)


	def additionalTrainSpam(self,path):
		self.spam_total += self.filesCounter(path) 

	def additionalTrainHam(self,path):
		self.ham_total += self.filesCounter(path)

	def dataCal(self):
		self.spam_list=self.spam_total.most_common()
		self.spam_list.append(('total_words',sum(self.spam_total.values())))
		self.spam_list.append(('words_size_s',len(self.spam_total)))
		self.spam_list.append(('file_size',self.spam_size))

		self.ham_list=self.ham_total.most_common()
		self.ham_list.append(('total_words',sum(self.ham_total.values())))
		self.ham_list.append(('words_size',len(self.ham_total)))
		self.ham_list.append(('file_size',self.ham_size))
		self.save_list=self.spam_list+self.ham_list





def main(argv):
	train_1 = Learner(argv[1])

		
if __name__ == '__main__':
	main(sys.argv)




