# Exercice 2 : simulateur de course de trot attelé
Une course de trot attelé rassemble 12 à 20 chevaux, chacun tractant un sulky, et 
étant mené par un driver. Elle peut faire l’objet d’un tiercé, d’un quarté, ou d’un 
quinté.  
La course est supposée se dérouler sur un hippodrome rectiligne (chaque cheval disposant de 
son propre couloir), d’une longueur de 2 400 m. Il est à noter que chaque cheval doit respecter 
l’allure du trot de bout en bout, le passage au galop entrainant sa disqualification.  
L’utilisateur saisit 
au démarrage le nombre de chevaux et le type de la courseLa course se déroule à la manière d’un « jeu de plateau » : à chaque tour de jeu, chaque cheval fait 
l’objet d’un jet de dé (à 6 faces), qui décide d’une altération possible de sa vitesse (augmentation, 
stabilisation, diminution). La nouvelle vitesse détermine alors la distance dont il avance. Chaque tour 
de jeu représente 10 secondes du déroulement de la course, mais le temps ne sera pas rendu dans le 
programme. C’est l’utilisateur qui fera avancer la course de tour en tour, à la suite d’un message du 
programme l’y invitant.