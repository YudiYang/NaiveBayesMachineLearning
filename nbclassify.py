#!/usr/bin/python


#####################Naive Bayes Classify#####################
#Class:  USC-EE599
#Author: Yudi Yang
#USC ID: 5017708933
#Email:  yudiyang@usc.edu
#Version: 1.0
#######################################################


import os,re,sys
import collections
import numpy as np

class Classifier():
	def __init__(self,filename,savename):
		'''
			load in the data which have already been trained.
		'''
		original_data = np.loadtxt(filename,str,delimiter = ',')
		dict_data = dict(original_data)
		split_len = int(dict_data['words_size_s'])+3
		self.trained_data_s = dict(original_data[:split_len])
		self.trained_data_h = dict(original_data[split_len:])			
		self.basicValues()
		self.filesCounter('./spam_or_ham_test',savename)

	def basicValues(self):

		self.total_words_s = float(self.trained_data_s['total_words'])
		self.total_words_h = float(self.trained_data_h['total_words'])
		self.file_size_s = float(self.trained_data_s['file_size'])
		self.file_size_h = float(self.trained_data_h['file_size'])
		self.p_Spam = (self.total_words_s)/(self.total_words_s+self.total_words_h)
		self.p_Ham = (self.total_words_h)/(self.total_words_s+self.total_words_h)

	def nbCal(self,counter):
		p_msg_spam = 0.0
		p_msg_ham = 0.0
		for i in counter:
			if( i in self.trained_data_s):
				p_msg_spam += float(self.trained_data_s[i])*float(counter[i])
			if( i in self.trained_data_h):
				p_msg_ham += float(self.trained_data_h[i])*float(counter[i])
		vacb = sum(counter.values())
		p_msg_spam = (p_msg_spam+vacb)/(self.total_words_s+vacb)
		p_msg_ham = (p_msg_ham+vacb)/(self.total_words_h+vacb)
		p_spam_msg = self.p_Spam * p_msg_spam/(self.p_Spam * p_msg_spam + self.p_Ham*p_msg_ham)
		p_ham_msg = self.p_Ham*p_msg_ham/(self.p_Spam * p_msg_spam + self.p_Ham*p_msg_ham)
		print p_spam_msg,p_ham_msg,'\n'
		if(p_spam_msg>p_ham_msg):
			return 'SPAM'
		elif(p_ham_msg>p_spam_msg):
			return 'HAM'
		else:
			return 'CANNOT DECIDE'


	def filesCounter(self,path,savename):
		result = []
		for file in os.listdir(path):
			if(file.endswith('.txt')):
				print '==============================\n'
				print 'DEALING WITH FILE: %s',file
				print '==============================\n'
				counter = self.getCounter(path+'/'+file)
				result.append(self.nbCal(counter))
		np.savetxt(savename,result,fmt='%s',delimiter='\n')


	def getCounter(self,filesource):
		'''Given a File, count all words in this file'''
		wordPattern = r'''[A-Za-z]+|\$?\d+%?$''' 		##this is the regular expression to find each word.
		fi = open(filesource)
		ri = re.findall(wordPattern,fi.read())						##get all words from the file
		return collections.Counter(ri)								##give back the result of counting words.
def main(argv):
	new_class = Classifier(argv[1],argv[2])
if __name__ == '__main__':
	main(sys.argv)