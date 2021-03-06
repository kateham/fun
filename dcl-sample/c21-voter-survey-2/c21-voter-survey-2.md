VOTER Survey - Part 2
================
Kate Ham
2020-02-18

  - [2016 vote by social and economic
    views](#vote-by-social-and-economic-views)
  - [Estimated size of groups](#estimated-size-of-groups)
  - [How groups’ vote changed between 2012 and
    2016](#how-groups-vote-changed-between-2012-and-2016)

``` r
# Libraries
library(tidyverse)
library(dcl)
library(knitr)

# Parameters
  # File with VOTER Survey data
file_voter_survey <- "../../data/voter-survey/data.rds"
  # File for answers
file_answers <- "../../data/voter-survey/answers_2.rds"

#===============================================================================

# Read in answers
answers <- read_rds(file_answers)
```

The [Democracy Fund Voter Study Group](https://www.voterstudygroup.org)
“is a research collaboration comprised of nearly two dozen analysts
and scholars from across the political spectrum offering new data and
analysis exploring American voter’s beliefs and behaviors.” They
commissioned the Views of the Electorate Research Survey (VOTER Survey)
after the 2016 U.S. presidential election. This was a survey of 8,000
voting-age adults on how they voted in both the 2012 and 2016
presidential elections together with the answers to over 600 other
questions. Researchers are using the data from this survey to seek
insights into the electorate and the 2016 election.

In Part 1, you derived variables on the views of those surveyed on
issues that were salient during the campaign. The result is in the file
`file_voter_survey`. In this part, you will visualize this data to seek
to understand the relationship of these views to how voters voted in the
2016 election and how their votes changed between 2012 and 2016.

## 2016 vote by social and economic views

Two of the derived variables were composites

  - `social`: Combination of views on moral issues, and views towards
    African-Americans, immigrants, and Muslims
  - `economic`: Combination of views on social safety net, trade,
    inequality, and the role of government

**q1** Create a presentation plot of `social` vs. `economic` together
with how each voter voted in the 2016 election. Why is this plot
misleading? Nevertheless, what insights does it provide, especially for
the Democrats?

<!-- Use following chunk for plot. -->

``` r
voter_survey <- read_rds(file_voter_survey)

voter_survey %>% 
  drop_na() %>% 
  ggplot(aes(social, economic, color = vote_2016)) +
  geom_point(alpha = 0.25) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  scale_color_manual(values = c("blue", "green", "red")) +
  annotate(
    geom = "label",
    x = c(-Inf, Inf, Inf, -Inf),
    y = c(Inf, Inf, -Inf, -Inf),
    label = c("Libertarian", "Conservative", "Populist", "Liberal"),
    hjust = c(-0.1, 1.2, 1, -0.1),
    vjust = c(1.5, 1.5, -0.5, -0.5)
  ) +
  labs(
    title = "Voter Views by 2016 Election Vote",
    color = "2016 Presidential \nElection Vote",
    caption = "Source: VOTER Survey",
    x = "Social Views",
    y = "Economic Views"
  )
```

<img src="c21-voter-survey-2_files/figure-gfm/q1-1.png" width="100%" />
This plot is misleading because each case is weighted by the US
population that it represents, according to the study; for example cases
with less weight are overrepresented in this plot.

Nonetheless, we observe that Clinton voters are socially and fiscally
liberal whereas Trump voters are socially and fiscally conservative.
More importantly, note that there are significant portions of Democrats
and Republicans that are populists. The Democrats, with Clinton as the
nominee, did not appeal to the socially conservative but economically
liberal voter base.

## Estimated size of groups

**q2.1** Each row of the dataset contains the data for a single
individual who was polled. From the individual’s demographic information
and the prevalence of these demographic characteristics in the sampled
population, pollsters can assign individuals weights. These weights can
then be used to adjust polls for non-representative sampling. For
example, suppose a poll consisted 40% women and 60% men. If the pollster
knows that the sampled population actually consists of 50% women and 50%
men, then they can give the women a weight of 5 / 4 and the men a weight
of 5 / 6. The weights are then used to make weighted averages of poll
responses.

The proportion of the popular vote in the 2016 presidential election was

| vote\_2016 |  prop |
| :--------- | ----: |
| Clinton    | 0.482 |
| Trump      | 0.461 |
| Other      | 0.057 |

Calculate the proportion of the vote for the candidates in the VOTER
Survey. How close are the results to the actual vote? Be sure to use
`weight`.

``` r
q2.1 <-
  voter_survey %>% 
  count(vote_2016, wt = weight) %>% 
  drop_na() %>% 
  mutate(
    prop = n/sum(n)
  ) %>% 
  select(-n)

# Print results
if (exists("q2.1")) q2.1 %>% arrange(desc(prop)) %>% kable(digits = 3)
```

| vote\_2016 |  prop |
| :--------- | ----: |
| Clinton    | 0.471 |
| Trump      | 0.462 |
| Other      | 0.067 |

``` r
# Compare result with answer
if (exists("q2.1")) compare(answers$q2.1, q2.1)
```

    ## TRUE

**q2.2** Now compute and visualize the size of each of the groups in
`group` by proportion. What conclusions can you draw?

``` r
q2.2 <- 
  voter_survey %>% 
  count(group, wt = weight) %>% 
  drop_na() %>% 
  mutate(
    prop =  n/sum(n)
  ) %>% 
  select(-n)

q2.2 %>% 
  mutate(group = fct_reorder(group, prop)) %>% 
  ggplot(aes(group, prop)) +
  geom_col()
```

<img src="c21-voter-survey-2_files/figure-gfm/unnamed-chunk-4-1.png" width="100%" />

``` r
# Print results
if (exists("q2.2")) q2.2 %>% arrange(desc(prop)) %>% kable(digits = 3)
```

| group        |  prop |
| :----------- | ----: |
| Liberal      | 0.399 |
| Populist     | 0.320 |
| Conservative | 0.229 |
| Libertarian  | 0.053 |

``` r
# Compare result with answer
if (exists("q2.2")) compare(answers$q2.2, q2.2)
```

    ## TRUE

There were very few libertarians, and in fact while one might suspect
conservatives and liberals to be the highest proportion since they are
rooted in the Republican and Democratic parties respectively, a
significant portion of 2016 voters are populists.

## How groups’ vote changed between 2012 and 2016

**q3.1** For each of the four groups in `group` calculate the proportion
of the group that voted for the Democratic candidate, the Republican
candidate, and Other candidates for both 2012 and 2016.

``` r
q3.1 <- 
  voter_survey %>% 
  drop_na(group, vote_2012, vote_2016) %>% 
  pivot_longer(
    cols = c(vote_2012, vote_2016),
    names_sep = "_",
    names_to = c("vote","year"),
    values_to = "party"
  ) %>% 
  transmute(
    case_identifier,
    weight,
    group,
    year = as.integer(year),
    party = 
      case_when(
        party %in% c("Obama", "Clinton") ~ "Democrat",
        party %in% c("Romney", "Trump") ~ "Republican",
        TRUE ~ "Other"
      )
  ) %>% 
  count(group, year, party, wt = weight) %>%
  group_by(year, group) %>% 
  mutate(
    prop = n/sum(n)
  ) %>% 
  select(-n) %>% 
  ungroup()

# Compare result with answer
if (exists("q3.1")) compare(answers$q3.1, q3.1)
```

    ## TRUE

**q3.2** For each group and each election, there were proportions of
votes cast for Democrat, Republican, and Other. Using `q3.1`, create a
presentation plot that shows for each group how these proportions
changed between 2012 and 2016. What conclusions can you draw?

<!-- Use following chunk for plot. -->

``` r
q3.1 %>% 
  ggplot(aes(factor(year), prop, color = party, group = party)) +
  geom_point() +
  geom_line(size = 1) +
  facet_wrap(~ group, nrow = 1) +
  scale_color_manual(values = c("blue", "green", "red")) +
  scale_x_discrete(expand = c(0.1, 0.1)) +
  scale_y_continuous(label = scales::label_percent(accuracy = 1)) +
  theme_minimal() +
  labs(
    title = "Change in Political Views by Party (2012 - 2016)",
    subtitle = "Republicans turn to populism, libertarians turn to third-party candidates",
    caption = "Source: VOTER Study",
    x = NULL,
    y = NULL
  )
```

<img src="c21-voter-survey-2_files/figure-gfm/q3.2-1.png" width="100%" />

After you finish this task, please complete [Notes on Task -
Part 1](https://forms.gle/NdSN5Tye6EtMiXAm8).
