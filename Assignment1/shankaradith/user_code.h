#ifndef USER_CODE_H
#define USER_CODE_H

#include <vector>
#include <string>
#include <utility>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <map>
#include "fileIterator.h"
#include "fileWriter.h"

using namespace std;

vector<string> split(const string &s, char delimiter){
    vector<string> tokens;
    string token;
    istringstream tokenStream(s);
    while (getline(tokenStream, token, delimiter)){
        tokens.push_back(token);
    }
    return tokens;
}

//#PROMPT# Create a global variable to store all the hashtags, i.e. a vector of pairs where each pair contains the product and its vector of hashtags
vector<pair<string,vector<string>>> globalproductHashtags;
//#PROMPT# Create another gloabl variable to check whether the globalproductHashtags has been initialized or not
bool globalproductHashtagsInitialized = false;


void groupCustomersByHashtags(fileIterator& hashtags, fileIterator& purchases, fileIterator& prices, int k, string outputFilePath)
{
    auto start = high_resolution_clock::now();

    // #PROMPT# Extract all the lines from the hashtags file and store them in an appropriate data structure
    vector<pair<string,vector<string>>> productHashtags;
    while(hashtags.hasNext()){
        string line = hashtags.next();
        vector<string> tokens = split(line,',');
        if (tokens.size() > 1) { // #PROMTP# Ensure there are hashtags present
            string product = tokens[0];
            vector<string> prodHashtags(tokens.begin() + 1, tokens.end());
            //#PROMPT# Make sure all prodHashtags are unique
            sort(prodHashtags.begin(), prodHashtags.end());
            prodHashtags.erase(unique(prodHashtags.begin(), prodHashtags.end()), prodHashtags.end());
            productHashtags.push_back(make_pair(product, prodHashtags));
        }
    }

    // #PROMPT# Extract all the lines from the purchases file and store them in an appropriate data structure
    vector<pair<string,string>> customerPurchases;
    while(purchases.hasNext()){
        string line = purchases.next();
        vector<string> tokens = split(line,',');
        if (tokens.size() == 2) { // #PROMPT# Ensure the line has both customer and product
            string customer = tokens[0];
            string product = tokens[1];
            customerPurchases.push_back(make_pair(customer, product));
        }
    }

    auto end_1 = high_resolution_clock::now();
    auto duration_1 = duration_cast<microseconds>(end_1 - start);
    // cout << "Time taken to read the files: "<< duration_1.count() << " microseconds" << endl;

    // #PROMPT# Make a map of customer id to an array of tuples
    map<string,vector<pair<string,int>>> customerHashtags;
    for(auto purchase : customerPurchases){
        string customer = purchase.first;
        string product = purchase.second;
        for(auto prodHashtags : productHashtags){
            if(prodHashtags.first == product){
                for(auto hashtag : prodHashtags.second){
                    if(customerHashtags.find(customer) == customerHashtags.end()){
                        vector<pair<string,int>> temp;
                        temp.push_back(make_pair(hashtag, 1));
                        customerHashtags[customer] = temp;
                    }
                    else{
                        bool found = false;
                        for(auto& tag : customerHashtags[customer]){
                            if(tag.first == hashtag){
                                tag.second++;
                                found = true;
                                break;
                            }
                        }
                        if(!found){
                            customerHashtags[customer].push_back(make_pair(hashtag, 1));
                        }
                    }
                }
            }
        }
    }

    // #PROMTP# Sort the hashtags based on the count and if count is equal, then hashtags should be ordered lexiographically
    for(auto& customer : customerHashtags){
        sort(customer.second.begin(), customer.second.end(), [](pair<string,int> a, pair<string,int> b){
            if(a.second == b.second){
                return a.first < b.first;
            }
            return a.second > b.second;
        });
    }

    // #PROMPT# For each customer, get the first k hashtags out
    map<string,vector<string>> customerTopKHashtags;
    for(auto customer : customerHashtags){
        vector<string> topK;
        for(int i = 0; i < k && i < customer.second.size(); i++){
            topK.push_back(customer.second[i].first);
        }
        customerTopKHashtags[customer.first] = topK;
    }
    //#PROMPT# Print the top k hashtags for each customer
    // for(auto customer : customerTopKHashtags){
    //     cout << customer.first << ": ";
    //     for(auto hashtag : customer.second){
    //         cout << hashtag << " ";
    //     }
    //     cout << endl;
    // }

    // #PROMPT# Create a map between the group id (int) and customer ids (vector of ints). The group id should be unique for each group. Add the first customer to group 1, check if the top k hashtags of the second customer are the same as the first customer, if yes, add the second customer to group 1, else add the second customer to group 2 and so on. The map should be group id to vector of customer ids.
    map<int, vector<int>> customerGroup;
    int group = 1;
    for(auto customer : customerTopKHashtags){
        bool found = false;
        for(auto& cgroup : customerGroup){
            if(customerGroup[cgroup.first].size() > 0){
                //#PROMTP# sort the hashtags and compare
                vector<string> first = customerTopKHashtags[to_string(customerGroup[cgroup.first][0])];
                vector<string> second = customer.second;
                sort(first.begin(), first.end());
                sort(second.begin(), second.end());
                if(first == second){
                    customerGroup[cgroup.first].push_back(stoi(customer.first));
                    found = true;
                    break;
            }
        }
        }
        if(!found){
            vector<int> temp;
            temp.push_back(stoi(customer.first));
            customerGroup[group] = temp;
            group++;
        }
    }

    // #PROMPT# Write the output to a file
    for(auto group : customerGroup){
        writeOutputToFile(group.second, outputFilePath);
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    // cout << "Time taken by compute part of the function: "<< duration.count() << " microseconds" << endl;

    // #PROMPT# Free all variables used from memory
    productHashtags.clear();
    customerPurchases.clear();
    customerHashtags.clear();
    customerTopKHashtags.clear();
    customerGroup.clear();
    
    // cout << "Function completed" << endl;
    return;
}

//////////////////////////////////////////////////////////////////////////////////
// MODIFY THIS SECTION
//////////////////////////////////////////////////////////////////////////////////
/**
 * @brief Modify this code to solve the assigment. Include relevant document. Mention the prompts used prefixed by #PROMPT#.
 *        
 * 
 * @param customerList 
 * @param purchases 
 * @param prices
 */
float calculateGroupAverageExpense(vector<int> customerList, fileIterator& purchases,fileIterator& prices){
    //Use this to log compute time    
    auto start = high_resolution_clock::now();
    //  Write your code here
    // This function calculates the (total price of products purchased by the customers in the group) / (number of customers in the group) for each group.
    // The customerList is a vector of integers where each integer represents a customer id, and all these customers are in the same group.
    // The purchases file contains the list of purchases made by each customer. Each line in the file contains two integers separated by a comma. The first integer is the customer id, and the second integer is the product id.
    // The prices file contains the price of each product. Each line in the file contains two integers separated by a comma. The first integer is the product id, and the second integer is the price of the product.
    // The function should return the average expense of the group.

    // #PROMPT# Extract all the lines from the purchases file and store them in an appropriate data structure
    vector<pair<int,int>> customerPurchases;
    while(purchases.hasNext()){
        string line = purchases.next();
        vector<string> tokens = split(line,',');
        if (tokens.size() == 2) { // #PROMPT# Ensure the line has both customer and product
            int customer = stoi(tokens[0]);
            int product = stoi(tokens[1]);
            customerPurchases.push_back(make_pair(customer, product));
        }
    }

    // #PROMPT# Extract all the lines from the prices file and store them in an appropriate data structure
    map<int,float> productPrices;
    while(prices.hasNext()){
        string line = prices.next();
        vector<string> tokens = split(line,',');
        if (tokens.size() == 2) { // #PROMPT# Ensure the line has both product and price
            int product = stoi(tokens[0]);
            float price = stof(tokens[1]);
            productPrices[product] = price;
        }
    }

    // #PROMPT# Calculate the total expense of the group
    float totalExpense = 0;
    for(auto purchase : customerPurchases){
        if(find(customerList.begin(), customerList.end(), purchase.first) != customerList.end()){
            totalExpense += productPrices[purchase.second];
        }
    }

    // #PROMPT# Calculate the average expense of the group
    float avgExpense = (float)totalExpense / customerList.size();

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    // cout << "Time taken by this function: "<< duration.count() << " microseconds" << endl;

    return avgExpense;
}


//////////////////////////////////////////////////////////////////////////////////
// MODIFY THIS SECTION
//////////////////////////////////////////////////////////////////////////////////
/**
 * @brief Modify this code to solve the assigment. Include relevant document. Mention the prompts used prefixed by #PROMPT#.
 *        
 * 
 * @param hashtags 
 * @param purchases 
 * @param prices
 * @param newHashtags
 * @param k
 * @param outputFilePath
 */
void groupCustomersByHashtagsForDynamicInserts(fileIterator& hashtags, fileIterator& purchases,fileIterator& prices,vector<string> newHashtags, int k, string outputFilePath){
    //Use this to log compute time    
    auto start = high_resolution_clock::now();
    //  Write your code here
    // This function is similar to the groupCustomersByHashtags function, but it adds hashtags dynamically.
    // The hashtags file contains the list of hashtags for each product. Each line in the file contains the product id followed by a comma-separated list of hashtags.
    // The purchases file contains the list of purchases made by each customer. Each line in the file contains two integers separated by a comma. The first integer is the customer id, and the second integer is the product id.
    // The prices file contains the price of each product. Each line in the file contains two integers separated by a comma. The first integer is the product id, and the second integer is the price of the product.
    // The newHashtags is a vector of strings where each string represents a line in the newhashtags file. Each line is a product id followed by a comma-separated list of hashtags.
    // The function should take this newHashtags vector and parse it so that each element in the vector is taken and added to the globalproductHashtags vector.
    // The function should then group customers based on the hashtags in the globalproductHashtags vector and write the output to the outputFilePath.
    // The function should return void.

    //#PROMPT# Check if the globalproductHashtags has been initialized or not, and if it has not been initialized, then initialize it
    if(!globalproductHashtagsInitialized){
        // #PROMPT# Extract all the lines from the hashtags file and store them in an appropriate data structure
        vector<pair<string,vector<string>>> productHashtags;
        while(hashtags.hasNext()){
            string line = hashtags.next();
            vector<string> tokens = split(line,',');
            if (tokens.size() > 1) { // #PROMPT# Ensure there are hashtags present
                string product = tokens[0];
                vector<string> prodHashtags(tokens.begin() + 1, tokens.end());
                // #PROMPT# Make sure all prodHashtags are unique
                sort(prodHashtags.begin(), prodHashtags.end());
                prodHashtags.erase(unique(prodHashtags.begin(), prodHashtags.end()), prodHashtags.end());
                productHashtags.push_back(make_pair(product, prodHashtags));
            }
        }
        globalproductHashtags = productHashtags;
        globalproductHashtagsInitialized = true;
        for(auto line : newHashtags){
            vector<string> tokens = split(line,',');
            if (tokens.size() > 1) { // #PROMPT# Ensure there are hashtags present
                string product = tokens[0];
                vector<string> newprodHashtags(tokens.begin() + 1, tokens.end());
                // #PROMPT# Make sure all prodHashtags are unique
                sort(newprodHashtags.begin(), newprodHashtags.end());
                newprodHashtags.erase(unique(newprodHashtags.begin(), newprodHashtags.end()), newprodHashtags.end());
                for(auto& prod : globalproductHashtags){
                    if(prod.first == product){
                        for(auto hashtag : newprodHashtags){
                            if(find(prod.second.begin(), prod.second.end(), hashtag) == prod.second.end()){
                                prod.second.push_back(hashtag);
                            }
                        }
                    }
                }
            }
        }
    }
    else{
        // #PROMPT# Add the new hashtags to the globalproductHashtags vector. To do this iterate over the newHashtags vector and for each product in the newHashtags vector, add the hashtags to the product in the globalproductHashtags vector. The product will be present in the globalproductHashtags vector as it has been initialized in the previous iteration.
        for(auto line : newHashtags){
            vector<string> tokens = split(line,',');
            if (tokens.size() > 1) { // #PROMPT# Ensure there are hashtags present
                string product = tokens[0];
                vector<string> newprodHashtags(tokens.begin() + 1, tokens.end());
                // #PROMPT# Make sure all prodHashtags are unique
                sort(newprodHashtags.begin(), newprodHashtags.end());
                newprodHashtags.erase(unique(newprodHashtags.begin(), newprodHashtags.end()), newprodHashtags.end());
                for(auto& prod : globalproductHashtags){
                    if(prod.first == product){
                        for(auto hashtag : newprodHashtags){
                            if(find(prod.second.begin(), prod.second.end(), hashtag) == prod.second.end()){
                                prod.second.push_back(hashtag);
                            }
                        }
                    }
                }
            }
        }
    }

    //#PROMPT# Print the globalproductHashtags
    // for(auto prod : globalproductHashtags){
    //     cout << prod.first << ": ";
    //     for(auto hashtag : prod.second){
    //         cout << hashtag << " ";
    //     }
    //     cout << endl;
    // }

    // #PROMPT# Extract all the lines from the purchases file and store them in an appropriate data structure
    vector<pair<string,string>> customerPurchases;
    while(purchases.hasNext()){
        string line = purchases.next();
        vector<string> tokens = split(line,',');
        if (tokens.size() == 2) { // #PROMPT#Ensure the line has both customer and product
            string customer = tokens[0];
            string product = tokens[1];
            customerPurchases.push_back(make_pair(customer, product));
        }
    }

    auto end_1 = high_resolution_clock::now();
    auto duration_1 = duration_cast<microseconds>(end_1 - start);
    // cout << "Time taken to read the files: "<< duration_1.count() << " microseconds" << endl;

    // #PROMPT# Extract all the lines from the prices file and store them in an appropriate data structure
    map<string,float> productPrices;
    while(prices.hasNext()){
        string line = prices.next();
        vector<string> tokens = split(line,',');
        if (tokens.size() == 2) { // #PROMPT# Ensure the line has both product and price
            string product = tokens[0];
            float price = stof(tokens[1]);
            productPrices[product] = price;
        }
    }

    // #PROMPT# Make a map of customer id to an array of tuples
    map<string,vector<pair<string,int>>> customerHashtags;
    for(auto purchase : customerPurchases){
        string customer = purchase.first;
        string product = purchase.second;
        for(auto prodHashtags : globalproductHashtags){
            if(prodHashtags.first == product){
                for(auto hashtag : prodHashtags.second){
                    if(customerHashtags.find(customer) == customerHashtags.end()){
                        vector<pair<string,int>> temp;
                        temp.push_back(make_pair(hashtag, 1));
                        customerHashtags[customer] = temp;
                    }
                    else{
                        bool found = false;
                        for(auto& tag : customerHashtags[customer]){
                            if(tag.first == hashtag){
                                tag.second++;
                                found = true;
                                break;
                            }
                        }
                        if(!found){
                            customerHashtags[customer].push_back(make_pair(hashtag, 1));
                        }
                    }
                }
            }
        }
    }

    // #PROMTP# Sort the hashtags based on the count and if count is equal, then hashtags should be ordered lexiographically
    for(auto& customer : customerHashtags){
        sort(customer.second.begin(), customer.second.end(), [](pair<string,int> a, pair<string,int> b){
            if(a.second == b.second){
                return a.first < b.first;
            }
            return a.second > b.second;
        });
    }

    // #PROMPT# For each customer, get the first k hashtags out
    map<string,vector<string>> customerTopKHashtags;
    for(auto customer : customerHashtags){
        vector<string> topK;
        for(int i = 0; i < k && i < customer.second.size(); i++){
            topK.push_back(customer.second[i].first);
        }
        customerTopKHashtags[customer.first] = topK;
    }
    //#PROMTP# Print the top k hashtags for each customer
    // for(auto customer : customerTopKHashtags){
    //     cout << customer.first << ": ";
    //     for(auto hashtag : customer.second){
    //         cout << hashtag << " ";
    //     }
    //     cout << endl;
    // }

    // #PROMPT# Create a map between the group id (int) and customer ids (vector of ints). The group id should be unique for each group. Add the first customer to group 1, check if the top k hashtags of the second customer are the same as the first customer, if yes, add the second customer to group 1, else add the second customer to group 2 and so on. The map should be group id to vector of customer ids.
    map<int, vector<int>> customerGroup;
    int group = 1;
    for(auto customer : customerTopKHashtags){
        bool found = false;
        for(auto& cgroup : customerGroup){
            if(customerGroup[cgroup.first].size() > 0){
                // #PROMPT# sort the hashtags and compare
                vector<string> first = customerTopKHashtags[to_string(customerGroup[cgroup.first][0])];
                vector<string> second = customer.second;
                sort(first.begin(), first.end());
                sort(second.begin(), second.end());
                if(first == second){
                    customerGroup[cgroup.first].push_back(stoi(customer.first));
                    found = true;
                    break;
            }
        }
        }
        if(!found){
            vector<int> temp;
            temp.push_back(stoi(customer.first));
            customerGroup[group] = temp;
            group++;
        }
    }

    // #PROMPT# Write the output to a file
    for(auto group : customerGroup){
        writeOutputToFile(group.second, outputFilePath);
    }

    
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    // cout << "Time taken by compute part of the function: "<< duration.count() << " microseconds" << endl;

    // Use the below utility function to write the output to a file
    // Call this function for every group as a vector of integers
    // vector<int> group;
    // writeOutputToFile(group, outputFilePath);

    // #PROMPT# Free all variables used from memory
    // productHashtags.clear();
    customerPurchases.clear();
    customerHashtags.clear();
    customerTopKHashtags.clear();
    customerGroup.clear();

    // cout << "Function completed" << endl;
    return;   
}

#endif // USER_CODE_H
