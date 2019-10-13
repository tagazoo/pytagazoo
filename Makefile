build_package:
	python3 setup.py build sdist bdist_wheel

build: build_package
	docker build -t test_py_tagazoo .

unittest: build 
	docker run -it --rm test_py_tagazoo

build_int: build_package
	docker build -t test_py_tagazoo_int -f Dockerfile.int .

int: build_int 
	docker run -it --rm --network isonet test_py_tagazoo_int

clear:
	rm -rf build dist *.egg-info