/*
 * midwife tracks files and folders created in a root directory.
 * Copyright (C) 2017  Massimiliano Patacchiola
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
*/

// Compile with: g++-7 -std=c++1z midwife.cpp -lstdc++fs -o ./midwife
// Usage: midwife --destination ./ --sleep 1000

#include <experimental/filesystem>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <thread>

#define VERSION "1.0.0"

/**
* Print the help message.
* @param name the name of the program (argv[0])
**/
static void show_usage(std::string name)
{
    std::cerr << "Usage: \n"
              << "\t" << name << " <option(s)>\n"
              << "Options:\n"
              << "\t-h, --help        \t Show this help message\n"
              << "\t-d, --destination \t Destination directory (default to ./)\n"
              << "\t-s, --sleep       \t Sleep between calls in millisec (default to 1000)\n"
              << "\t-v, --version     \t Print the name and version\n"
              << std::endl;
}

/**
* Initialization, first iteration of the destination folder.
* It finds the files which are used for comparison later.
* @param path
* @return rPathsVector
**/
int initialize(std::string path, std::vector<std::experimental::filesystem::v1::directory_entry>& rPathsVector){
    std::experimental::filesystem::path aPath {path};
    int totalCounter = 0;
    for (auto & p : std::experimental::filesystem::recursive_directory_iterator(aPath)){
        rPathsVector.push_back(p);
        totalCounter += 1;
        //std::cout << "Path: " << p << std::endl;
        //std::cout << "Parent path: " << aPath.parent_path() << endl;
        //std::cout << "Filename: " << aPath.filename() << endl;
        //std::cout << "Extension: " << aPath.extension() << endl;
        //std::cout << endl;     
    }
    return totalCounter;
}

/**
* Using a list of paths check if there is a new element.
* It uses the list updated in the function initialization().
* @param path
* @return rPathsVector
**/
void find_intruse(std::string path, std::vector<std::experimental::filesystem::v1::directory_entry>& rPathVector){
    std::experimental::filesystem::path aPath {path};
    std::vector<std::experimental::filesystem::v1::directory_entry> newbornPathVector;
    for (auto & p : std::experimental::filesystem::recursive_directory_iterator(aPath)){
        if ( std::find(rPathVector.begin(), rPathVector.end(), p) == rPathVector.end() ){
             newbornPathVector.push_back(p);
             std::cout << p.path() << std::endl;
             //std::cout << std::experimental::filesystem::system_complete(p) << std::endl;
        }
     }
    rPathVector.insert(rPathVector.end(), newbornPathVector.begin(), newbornPathVector.end());
}


int main(int argc, char* argv[])
{
    // Set the variables  
    std::string pathToScan = std::experimental::filesystem::current_path(); //get current absolute path
    int sleep = 1000; //sleep in milliseconds

    //Check the parameters in input
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        //Check for the help parameter
        if ((arg == "-h") || (arg == "--help")) {
            show_usage(argv[0]);
            return 0;
        //Check for the destination parameter
        } else if ((arg == "-d") || (arg == "--destination")) {
            if (i + 1 < argc) { // Make sure we aren't at the end of argv!
                pathToScan = argv[i+1]; // Increment 'i' so we don't get the argument as the next argv[i].
                if(!std::experimental::filesystem::is_directory(pathToScan)){
                std::cerr << "--destination option requires a valid path." << std::endl;
                return -1;
                }
            } else { // Uh-oh, there was no argument to the destination option.
                std::cerr << "--destination option requires one argument." << std::endl;
                return -1;
            }
        //Check for the sleep parameter
        } else if ((arg == "-s") || (arg == "--sleep")) {
            if (i + 1 < argc) {
                try{
                    std::string sleep_string = argv[i+1];
                    sleep = std::stoi(sleep_string);
                } catch (const std::invalid_argument& ex) {
                    std::cerr << "--sleep option requires a valid positive integer." << std::endl;
                    return -1;
                }               
            } else {
                  std::cerr << "--sleep option requires one argument." << std::endl;
                return -1;
            }  
        //Check for the version parameter
        } else if ((arg == "-v") || (arg == "--version")) {
            std::cerr << "midwife" << " version " << VERSION << std::endl;
            return 0; 
        }
    }


    std::vector<std::experimental::filesystem::v1::directory_entry> pathVector;
    int totalCounter = 0;

    // Initialization: it counts the folders and files
    totalCounter = initialize(pathToScan, pathVector);
    //std::cout << "Total ..... " << totalCounter << std::endl;

    //Main loop
    while(1){
        std::this_thread::sleep_for(std::chrono::milliseconds(sleep));
        find_intruse(pathToScan, pathVector);
    }

    return 0;
}
