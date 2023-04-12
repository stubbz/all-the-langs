package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type SomeRequest struct {
	SKU      string `json:"sku"`
	Quantity int    `json:"quantity"`
}

func addToCartV1(c *gin.Context) {
	var request SomeRequest

	if bindingResult := c.ShouldBindJSON(&request); bindingResult != nil {

		c.JSON(http.StatusBadRequest, gin.H{"error": bindingResult.Error()})
	} else {
		response := gin.H{
			"status": "success",
			"data":   request,
		}
		c.JSON(http.StatusOK, response)
	}
}

// playing around with a somewhat generic handler
func tryHandleJSON(c *gin.Context, handleRequest func(*gin.Context, any) gin.H) {
	var request SomeRequest
	if bindingResult := c.ShouldBindJSON(&request); bindingResult != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": bindingResult.Error()})
	} else {
		response := handleRequest(c, request)
		c.JSON(http.StatusOK, response)
	}
}

func addToCartV2(c *gin.Context) {
	tryHandleJSON(c, func(c *gin.Context, request any) gin.H {
		return gin.H{
			"status": "success",
			"data":   request,
		}
	})
}

func main() {
	r := gin.Default()

	r.POST("/addToCart", addToCartV1)
	r.POST("/addToCart2", addToCartV2)

	r.Run(":8080")
}
