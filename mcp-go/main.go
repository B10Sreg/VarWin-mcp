package main

import (
	"io"
	"log"
	"os"
	"path/filepath"
	"runtime"

	"varwin-mcp/internal/server"
)

func main() {
	// Setup log directory
	var logDir string
	if runtime.GOOS == "windows" {
		if appData := os.Getenv("APPDATA"); appData != "" {
			logDir = filepath.Join(appData, "VarwinData18", "Logs")
		} else {
			homeDir, _ := os.UserHomeDir()
			logDir = filepath.Join(homeDir, "AppData", "Roaming", "VarwinData18", "Logs")
		}
	} else {
		homeDir, _ := os.UserHomeDir()
		logDir = filepath.Join(homeDir, ".config", "VarwinData18", "Logs")
	}

	_ = os.MkdirAll(logDir, 0755)
	logFile, err := os.OpenFile(filepath.Join(logDir, "mcp_server_go.log"), os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err == nil {
		log.SetOutput(io.MultiWriter(os.Stderr, logFile))
	} else {
		log.SetOutput(os.Stderr)
	}

	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
	log.Println("Varwin MCP Go Server starting on STDIN...")

	srv := server.NewServer()
	srv.RunStdio()
}
