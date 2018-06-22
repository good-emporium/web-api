build:
	dep ensure
	env GOOS=linux go build -ldflags="-s -w" -o bin/organization/create/main.go
	env GOOS=linux go build -ldflags="-s -w" -o bin/organization/get/main.go
	env GOOS=linux go build -ldflags="-s -w" -o bin/organization/get-multiple/main.go
