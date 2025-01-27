import email
import re
import math
import numpy as np
import matplotlib.pyplot as plt

def read_file(fname):
    """ Lit un fichier compose d'une liste de emails, chacun separe par au moins 2 lignes vides."""
    f = open(fname,'rb')
    raw_file = f.read()
    f.close()
    raw_file = raw_file.replace(b'\r\n',b'\n')
    emails =raw_file.split(b"\n\n\nFrom")
    emails = [emails[0]]+ [b"From"+x for x in emails[1:] ]
    return emails

def get_body(em):
    """ Recupere le corps principal de l'email """
    body = em.get_payload()
    if type(body) == list:
        body = body[0].get_payload()
    try:
        res = str(body)
    except Exception:
        res=""
    return res

def clean_body(s):
    """ Enleve toutes les balises html et tous les caracteres qui ne sont pas des lettres """
    patbal = re.compile('<.*?>',flags = re.S)
    patspace = re.compile('\W+',flags = re.S)
    return re.sub(patspace,' ',re.sub(patbal,'',s))

def get_emails_from_file(f):
    mails = read_file(f)
    return [ s for s in [clean_body(get_body(email.message_from_bytes(x))) for x in mails] if s !=""]

spam = get_emails_from_file("spam.txt" )
nospam = get_emails_from_file("nospam.txt")

"""
for s in spam:
	print (s)
"""

def split(liste, x):
	l1 = []
	l2 = []
	pivot = math.floor(len(liste)*x)
	
	l1 = liste[0:pivot]
	l2 = liste[pivot:]
	
	return l1, l2



#np.bin

def longueur_body(em):

	return len(em)
	
#print(longueur_body(l1[0]))

#pour calculer l'histogramme des longeur de mails
def liste_longueur(lem):
	li=[]
	for l in lem:
		li.append(longueur_body(l))
		
	return li
"""
liste = liste_longueur(l1)
length = len(liste)
plt.hist(liste,bins=int(length/20))
"""
#Q 2.3
def apprend_modele(spam, non_spam):
	#renvoie la proba qu'un email soit d'une longueur donnee sachant que c'est un spam
	#p(X=x | Y=+1) = p(Y=+1 | X=x) * p(X=x) / p(Y=+1)
	#or p(Y=+1) = 0.5
	#et p(X=x) = nbr email de longueur x / nbr email
	#et p(Y=+1 | X=x) = nbr email spam de taille x / nbr longueur de taille x
	
	#renvoyer la distribution des spam selon leur longueur x
	
	#calculs:
	#suppression des doublons dans les listes
	liste_mails = liste_longueur(list(set(spam+non_spam)))
	#tableau (longueur, proba)
	dict_lp = []#dictionnaire longueur, proba spam
	
	for x in liste_mails:
		dict_lp.append((x,distribution(spam, non_spam, x)))
	
	return dict_lp
	


def distribution(spam, non_spam, x):
	#renvoie p(X=x | Y=+1) pour une longueur x donnee
	nb_x_spam = 0 #nbre de spam de longueur x
	nb_x_tot = 0 #nbre total de mail de llongueur x
	
	for lm in liste_longueur(spam):
		if (lm == x):
			nb_x_spam += 1
			nb_x_tot += 1
	for lm in liste_longueur(non_spam):
		if (lm == x):
			nb_x_tot += 1
	
	px = float(nb_x_tot) / (nb_x_tot + nb_x_spam) #p(X=x)
	pyx = float(nb_x_spam) / nb_x_tot #p(Y=+1 | X=x)
	
	pxy = pyx * px / 0.5 #p(X=x | Y=+1)
	
	return pxy
	
def predict_email(emails, modele):
	#renvoie la liste des labels pour l'ensemble des emails en fonction du modele passe en parametre

	labels = [] #labels[i] contient le label de l'email emails[i]
	#emails contient la longueur des emails
	for e in emails:
		
		proba=0.5
		for m in modele:
			if(e>=m[0] and e<m[1]):
				proba=m[2]
		
		if (proba > 0.5):
			labels.append(+1)
		else:
			labels.append(-1)
	
	return labels
	

#Q 2.4 P(f(x) = y)
def accuracy(emails, modele):
	#emails[i] = (email, label)
	list_email = []
	for e in emails:
		list_email.append(e[0])
		
	labels=predict_email(list_email,modele)
	cpt=0.0
	
	for i in range(len(labels)):
		if(l*emails[i][1]>=0):
			cpt+=1.0
	
	return cpt/len(labels)
	
	
	
def proba_err(emails,modele):

	return (1.0-accuracy(emails,modele))
	
def regroup(modele, bins):
	#la longueur du plus long mail
	
	modele=sorted(modele,key=lambda model: model[0], reverse=True)
	
	new_modele=[]
	proba=1.0
	l_max = modele[0][0]
	step=int(l_max/bins)
	
	cpt=0;
	
	for i in range(0, l_max,step):
			
			for m in modele:
				
				if(m[0]>=i and m[0]<i+step):
					proba*=m[1]
					cpt+=1
					
			if(cpt>0):
				new_modele.append((i,i+step,proba))
			
			else:
				new_modele.append((i,i+step,0.5))
				
			proba=1.0
			cpt=0
	
	return new_modele
		
		

l1_s,l2_s=split(liste_longueur(spam), 0.5)
l1_ns,l2_ns=split(liste_longueur(nospam), 0.5)	
	
	
modele=apprend_modele(l1_s,l1_ns)

emails=[]

for l in l2_s:
	emails.append((l,+1))
for l in l2_ns:
	emails.append((l,-1))
	
modele_bine=regroup(modele,len(modele)/20)
	
print(proba_err(emails,modele_bine))

plt.show()
