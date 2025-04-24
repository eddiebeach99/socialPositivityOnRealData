library(tidyverse)

process_data <- function(data) {
  data$alpha <- round(data$alpha1, 1)
  data$alpha2 <- round(data$alpha2, 1)
  
  plotData <- data %>% 
    group_by(alpha, alpha2) %>% 
    summarize(score = mean(score), .groups = 'drop')
  
  best_eq <- data %>% 
    group_by(alpha, alpha2) %>% 
    summarize(score = mean(score), .groups = 'drop') %>% 
    filter(alpha == alpha2)
  
  return(list(plotData = plotData, best_eq = best_eq))
}

create_plot <- function(plotData, best_eq) {
  ggplot(plotData, aes(x = alpha2, y = alpha, color = score, fill = score)) +
    geom_tile() +
    geom_abline() +
    geom_point(data = subset(plotData, score == max(plotData$score)), 
               aes(x = alpha2, y = alpha), color = "red", size = 3, shape = 8) +
    geom_point(data = subset(best_eq, score == max(best_eq$score)), 
               aes(x = alpha2, y = alpha), color = "black", size = 3, shape = 1) +
    scale_color_viridis_c(name = "Score") +
    scale_fill_viridis_c(name = "Score") +
    labs(x = expression(alpha["-"]), y = expression(alpha["+"])) +
    theme_classic() +
    theme(text = element_text(size = 18),
          axis.title = element_text(size = 16),
          axis.text = element_text(size = 18),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18), 
          aspect.ratio = 1,
          axis.text.x = element_text(angle = 45, vjust = 0.5, hjust = 0.5))
}

amazon_poor <- create_plot(plotDataAmazonPoor, best_eqAmazonPoor)
amazon_rich <- create_plot(plotDataAmazonRich, best_eqAmazonRich)
goodreads_poor <- create_plot(plotDataGoodreadsPoor, best_eqGoodreadsPoor)
goodreads_rich <- create_plot(plotDataGoodreadsRich, best_eqGoodreadsRich)
google_poor <- create_plot(plotDataGooglePoor, best_eqGooglePoor)
google_rich <- create_plot(plotDataGoogleRich, best_eqGoogleRich)
yelp_poor <- create_plot(plotDataYelpPoor, best_eqYelpPoor)
yelp_rich <- create_plot(plotDataYelpRich, best_eqYelpRich)

agg_poor <- bind_rows(
  plotDataAmazonPoor,
  plotDataGoodreadsPoor,
  plotDataGooglePoor,
  plotDataYelpPoor
) %>%
  group_by(alpha, alpha2) %>%
  summarize(score = mean(score), .groups = 'drop')

agg_rich <- bind_rows(
  plotDataAmazonRich,
  plotDataGoodreadsRich,
  plotDataGoogleRich,
  plotDataYelpRich
) %>%
  group_by(alpha, alpha2) %>%
  summarize(score = mean(score), .groups = 'drop')

best_eq_poor <- agg_poor %>% filter(alpha == alpha2)
best_eq_rich <- agg_rich %>% filter(alpha == alpha2)

agg_poor_plot <- create_plot(agg_poor, best_eq_poor) 

agg_rich_plot <- create_plot(agg_rich, best_eq_rich)



create_bias_plot <- function(poor_plotData, poor_best_eq, rich_plotData, rich_best_eq, rec_percent) {
  poor_bias <- poor_plotData %>% 
    mutate(bias = round(alpha - alpha2, 1)) %>%  
    group_by(bias) %>% 
    summarize(poor_score = mean(score), .groups = 'drop')
  
  rich_bias <- rich_plotData %>% 
    mutate(bias = round(alpha - alpha2, 1)) %>% 
    group_by(bias) %>% 
    summarize(rich_score = mean(score), .groups = 'drop')
  

  combined <- full_join(poor_bias, rich_bias, by = "bias") %>%
    mutate(
      weighted_score = (poor_score * rec_percent[1]/100 + rich_score * rec_percent[2]/100),
      type = "Weighted"
    )
  
  plot_data <- bind_rows(
    poor_bias %>% mutate(score = poor_score, type = "Poor") %>% select(bias, score, type),
    rich_bias %>% mutate(score = rich_score, type = "Rich") %>% select(bias, score, type),
    combined %>% select(bias, score = weighted_score, type)
  )
  
  ggplot(plot_data, aes(x = bias, y = score, color = type)) +
    geom_point(size = 1.5) +
    geom_line() +
    scale_color_manual(values = c("Poor" = "lightblue", "Rich" = "orange", "Weighted" = "purple")) +
    scale_x_continuous(
      breaks = seq(-1, 1, by = 0.5), 
      labels = sprintf("%.2f", seq(-1, 1, by = 0.5))
    ) +
    labs(x = "Bias", y = "Score", color = "") +
    theme_classic() +
    theme(
      text = element_text(size = 18),
      axis.title = element_text(size = 18),
      axis.text = element_text(size = 18),
      axis.text.x = element_text(angle = 45, vjust = 0.5, hjust = 0.5),
      legend.text = element_text(size = 18),
      legend.title = element_text(size = 16), 
      aspect.ratio = 1
    )
}
# Recommendation percentages caluclated from data_distribution_plots.ipynb
amazon_rec <- c(18.3, 81.7)
goodreads_rec <- c(12, 88)
google_rec <- c(9.1, 90.9)
yelp_rec <- c(25.6, 74.4)
agg_rec <- c(16.3, 83.7)

amazon_bias <- create_bias_plot(plotDataAmazonPoor, best_eqAmazonPoor, 
                                plotDataAmazonRich, best_eqAmazonRich, amazon_rec)
goodreads_bias <- create_bias_plot(plotDataGoodreadsPoor, best_eqGoodreadsPoor, 
                                   plotDataGoodreadsRich, best_eqGoodreadsRich, goodreads_rec)
google_bias <- create_bias_plot(plotDataGooglePoor, best_eqGooglePoor, 
                                plotDataGoogleRich, best_eqGoogleRich, google_rec)
yelp_bias <- create_bias_plot(plotDataYelpPoor, best_eqYelpPoor, 
                              plotDataYelpRich, best_eqYelpRich, yelp_rec)
agg_bias_plot <- create_bias_plot(agg_poor, best_eq_poor, agg_rich, best_eq_rich, agg_rec)


normativity_with_bias <- plot_grid(
  amazon_poor, goodreads_poor, google_poor, yelp_poor, agg_poor_plot,
  amazon_rich, goodreads_rich, google_rich, yelp_rich, agg_rich_plot,
  amazon_bias, goodreads_bias, google_bias, yelp_bias, agg_bias_plot,
  ncol = 5, 
  align = "hv",
  rel_heights = c(1, 1, 1)
)

ggsave("C:/Users/edwar/OneDrive/Uni/WiSe2024/Laborpraktikum/socialPositivityRealData/Plots/normativity_with_bias_rounded.png", 
       width = 24, height = 10)

#save.image(file = "C:/Users/edwar/OneDrive/Uni/WiSe2024/Laborpraktikum/socialPositivityRealData/Analysis/parameters.RData")