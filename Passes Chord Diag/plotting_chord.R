install.packages('circlize')
library(circlize)

home_data <- read.csv('home_pass.csv')
away_data <- read.csv('away_pass.csv')

chordDiagram(home_data)
chordDiagram(away_data)