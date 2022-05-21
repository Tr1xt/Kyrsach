import re
from tqdm.gui import trange

class svert:
	def __init__(self):

		self.kolvo_summatorov = 2
		self.summatori = [['1','2'],['1','3']]
		self.registr = [0,0,0]
		self.tabl = {}
		self.bits = 0
		self.d = []
		self.sborstroki = {}
		self.code = ''
		self.decode = ''

	def text_to_bits(self,text, encoding='utf-8', errors='surrogatepass'):
		self.bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
		self.bits = self.bits.zfill(8 * ((len(self.bits) + 7) // 8))
		return self.bits


	def _summatori_(self):
		for i in range(self.kolvo_summatorov):
			self.d.append(self.summatori[i])
		return self.d

	def _registr_(self,text):
		for perebor in range(len(self.text_to_bits(text))+len(self.registr)):
			del self.registr[-1]
			if perebor < len(self.text_to_bits(text)):
				self.registr.insert(0,int(self.text_to_bits(text)[perebor]))
			else:
				self.registr.insert(0,0)
			kod = ''
			for j in range(self.kolvo_summatorov):
				m = 0
				for k in range (len(self._summatori_()[j])):
					m += self.registr[int(self._summatori_()[j][k])-1]
				kod += str(m%2)
			self.sborstroki[perebor] = {}
			self.sborstroki[perebor][''.join(map(str,self.registr))] = str(kod)
			self.tabl[''.join(map(str,self.registr))] = str(kod)
		return self.sborstroki,self.tabl

	def _encode_(self,text):
		schet = 0
		for i in self._registr_(text)[0].values():
			if schet < len(self.text_to_bits(text)):
				schet += 1
				for j in i.values():
					self.code += str(j)
			else:
				break

		return self.code 

	def vslovare(self,registrdec):
		for i in self.tabl.keys():
			if list(i) == registrdec:
				return i

	def to_bits(self,code):
		registrdec = []
		for i in range(3):
			registrdec.append('0')
		for i in range(0,len(code),self.kolvo_summatorov):
			del registrdec[-1]
			registrdec.insert(0,'1')
			if code[i:i+int(self.kolvo_summatorov)] == self.tabl.get(self.vslovare(registrdec)):
				self.decode += '1'
			else:
				del registrdec[0]
				registrdec.insert(0,'0')
				if code[i:i+int(self.kolvo_summatorov)] == self.tabl.get(self.vslovare(registrdec)):
					self.decode += '0'
		return self.decode

	def _decode_(self,code,encoding='utf-8', errors='surrogatepass'):
		n = int(self.to_bits(code), 2)
		return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'