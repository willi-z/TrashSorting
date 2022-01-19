# TrashSorting
> Sorting Trash for Recycling
---

## Useage

1. Launch database with `docker-compose up`
2. (Optional) open [Kibana](http://localhost:5601/)
3. (Optional) add Data manually or by scraping Databases
4. (Optional) run Tree-Regression to develop sorting strategy

## Database-Design

1. Materials ("Chemestry", Metalls, Alloys) (Source: [Fig 5](https://onlinelibrary.wiley.com/doi/full/10.1002/advs.201900808))
![](https://onlinelibrary.wiley.com/cms/asset/002cd75b-39b4-4441-a32b-a9e27dc17550/advs1265-fig-0005-m.jpg)
   1. 0-dim
   2. 1-dim
   3. 2-dim
   4. 3-dim
3. Composites ()
4. Reactions

## Literature

### Databases

- [Research Databases](https://github.com/blaiszik/Materials-Databases)
- [Commercial DataBases](https://matmatch.com/resources/blog/material-database/)
- [University Texas Overview](https://guides.lib.utexas.edu/materials/data)
- [Paper: Data-Driven Materials Science: Status, Challenges, and Perspectives](https://onlinelibrary.wiley.com/doi/full/10.1002/advs.201900808)
  - [AFLOW](aflowlib.org)
  - [Computational Materials Repository](cmr.fysik.dtu.dk)
  - [Crystallography Open Database](crystallo-graphy.net)
  - [HTEM](htem.nrel.gov)
  - [Khazana](khazana.gatech.edu)
  - [MARVEL NCCR](nccr-marvel.ch)
  - [Materials Project](materials-project.org)
  - [MatNavi/NIMS](mits.nims.go.jp)
  - [NOMAD CoE](nomad-coe.eu)
  - [Open Quantum Materials Database](oqmd.org)
  - [Open Materials Database](openmaterialsdb.se)
  - [SUNCAT](suncat.stanford.edu)
- [Material-Toolbox](https://www.engineeringtoolbox.com/material-properties-t_24.html)

### Decision Trees

- [Wikipedia](https://en.wikipedia.org/wiki/Decision_tree_learning)
- [Entropy](https://towardsdatascience.com/entropy-how-decision-trees-make-decisions-2946b9c18c8)
- [Regression Trees](https://builtin.com/data-science/regression-tree)
- [Classification Trees]
- [Quinlan]
- [Beimann]

## Software

- [Scikit-Learn](https://scikit-learn.org/stable/index.html) 
  - [Decission Trees](https://scikit-learn.org/stable/modules/tree.html)
- [Optuna](https://github.com/optuna/optuna)


## Journals

- [Internaltional Journal of Computer Applications](https://www.ijcaonline.org/)