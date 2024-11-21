# [Dev IA GRETA / Lécroart Antoine](https://github.com/Dev-IA-2024/antoine.lecroart)

[↩️](..)
---

## Trucs utiles

---
### SHORTCUTS

#### F STring

nb = 23
age = "ans"

print(f"Salut j'ai {nb} {age}")
ou
x = f"Salut j'ai {nb} {age}"

---

#### Unpacking

tup = (1, 2, 3, 4, 5)
lst = [1, 2, 3, 4]
dic = {1: 'a', 2: 'b'}
coords = [4, 5]

a, b, c, d, e = tup
x, y = coords
a, b = dic     -> a = (1 'a')
a, b = dic.values()  -> a = 'a'
a, b = dic.items()  -> a = (1, 'a')

---

#### Multiple assignement

width, height = 400, 500

temp = width
width = height ---> width, height = height, width
height = temp

---

#### Comprehensions

x = [0 for i (ou _) in range(100)] --> remplit x avec cents 0, _ est une valeur dont on ne se servira pas

x = [i*j for i in range(100) for j in range(10)]

x = [[0 for _ in range(5)] for _ in range (10)]   ----> Nested list: liste [0,0,0,0,0] stocké dans une liste 10 fois : [[0,0,0,0,0], [0,0,0,0,0], ...]

---

#### Inline/ Ternary Condition

x = 1 if 2 > 3 else 0

---

#### Zip

names = ['tim', 'joe', 'Leo', 'Lea', 'tom']
ages = [21, 30, 19, 25]
eye_color = ['blue', 'yellow', 'red', 'brown']

print(list(zip(names, ages, eye_color)))  --> [('tim', 21, 'blue'), ('joe', 30, 'yellow'), ('Leo', 19, 'red'), ('Lea', 25, red)] ---> Tom ignoré car inassociable 

---

#### *args

lst = [1, 2]

def fonction (x, y):

fonction(*lst) ---> convertit lst en ses 2 composants pour les donner à  la fonction

---
---

### Méthodes list

liste.append() : ajoute à  la fin

liste.extend([1,2,3,....]) : append()  pour plusieurs

liste.insert() : insert(position, quoi inserer)

liste.remove() : supprime le contenu indiqué. EX: remove('lol') ou remove (1) <- retire l'élément 1, pas l'élément à  la position 1

liste.pop() :  supprime le dernier terme

slice : liste[:4] <- Début jusqu'à  4 / liste[2:4] <- entre 2 et 4 / liste[:] <- tout

liste.reverse() : Change la liste pour mettre à  l'envers.  print(liste[::-1] pour afficher à  l'envers sans modifier

liste.len() : longueur de la liste

max(liste) & min(liste) : valeur max et min dans la liste

liste.count(a) : compte le nombre de (a) dans la liste

liste.index('a') : renvoit la position ou se trouve 'a'

liste.sort() : met dans l'ordre croissant (ou sorted(liste))


---
---
![Baby Yoda](https://images3.alphacoders.com/110/1108129.jpg)
