## Disease Surveillance Dashboard

### Local environment setup

#### Install virtualenvwrapper
You can create virtual environment with  [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/stable/).

#### Clone the repository
``` bash
$ git clone https://github.com/chai-moz-dsd/chai.git
```

#### Create an virtual environment
*Example 1 - Using virtualenvwrapper*
``` bash
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv dsd
$ workon dsd
```
*Example 2 - Using virtualenv within project directory*
``` bash
$ virtualenv dsd
$ source dsd/bin/activate
```

#### Install neccessary packages
``` bash
$ pip install -r requirements.txt
```

#### Run Server
``` bash
$ ./go rs
```

#### Run unit tests
``` bash
$ ./go ut
```

#### Run functional tests
``` bash
$ ./go ft
```
