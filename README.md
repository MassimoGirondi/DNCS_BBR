# BBR performance analysis

This repository contains all the material used to obtain the results contained
in the [presentation](presentation/presentation.pdf).

This work has been done as part of the exam for the course Design of Networks and
Communication System, yield by Prof. Granelli at the University of Trento.

## How to use
* Install Vagrant
* Clone this repository
* Provision the machine with `vagrant up`
* Connect to the machine through `vagrant ssh` and install Mininet through the [`install_mininet.sh`](install_mininet.sh) script
* `cd` into any folder and run the tests.
* If you want some plots, tun the Python scripts in each folder after the tests

## Outcomes

The results are presented in the [presentation](presentation/presentation.pdf).

We could say that the expectations were correct and, overall, BBR achieves higher bandwidth
than other congestion control algorithm.

## License

All the files are licensed under the GNU GPL v3 license. See [LICENSE](LICENSE) for more details.

