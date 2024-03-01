library(spatstat)
library(jsonlite)

# Define the dimensions of the window (rectangle in this case)
xrange <- c(0, 2)  # Range of x coordinates
yrange <- c(0, 2)  # Range of y coordinates

# Specify the range for lambda values
lambda_min <- 1
lambda_max <- 5
n <- 10

# Generate n random lambda values within the specified range
lambda_values <- runif(n, min = lambda_min, max = lambda_max)

# Create an empty list to store point clouds
point_clouds <- list()

for (i in 1:n) {
  # Generate a rectangle window
  window <- owin(xrange, yrange)
  
  # Set the intensity parameter for the Poisson process
  lambda <- lambda_values[i]  # Intensity parameter for this instance
  
  # Generate points from a Poisson point process within the window
  poisson_points <- rpoispp(lambda * area.owin(window), win = window)
  
  # Extract x and y coordinates of each point
  points_array <- cbind(poisson_points$x, poisson_points$y)
  
  # Add points to the list with lambda as key
  point_clouds[[as.character(lambda)]] <- points_array
}

# Convert the list to JSON
json_data <- toJSON(point_clouds)

# Write JSON to a file
write(json_data, "point_clouds.json")