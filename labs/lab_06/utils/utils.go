package utils

import (
	"bufio"
	"os"
	"strings"
)

func Scan() string {
	var reader = bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	text = strings.TrimSpace(text)
	return text
}
