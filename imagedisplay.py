
def image_pipeline():
    #establish base variables 
    cwd = os.getcwd()
    cwd += "\Videos"

    #move into the appropriate directory
    os.chdir(cwd)

    #generate the list of files and folders in the Videos folder
    directories = os.listdir(cwd)
    directories= directories[::2] #we're assuming the only things in this folder are our video files and their related subfolders


        #only go through the top level folders for each video clip, not the subfolders' folders
    for directory in directories:
        path_vid_subfolder = cwd + "\\" + directory
        os.chdir(path_vid_subfolder)
       
        #for each subfolder do an action 
        for subfolder in subfolders: 

            subfolder_path = path_vid_subfolder+"\\"+subfolder
            #check that the subfolder doesn't already exist and if it doesn't create it and run the appropriate action
            if not os.path.exists(subfolder_path):

                os.mkdir(subfolder)

                if subfolder == raw_subfolder:
                    pass                    
                elif subfolder == diff_subfolder:
                    image_diff(os.getcwd(),subfolder)
                elif subfolder == segmented_subfolder:
                    image_segmentation(os.getcwd(),subfolder)
                elif subfolder == canny_subfolder:
                    canny_edge(os.getcwd(),subfolder,'raw')
                elif subfolder == cannydiff_subfolder:
                    canny_edge(os.getcwd(),subfolder,'diff')

        #after processing the photos return to the Video folder
        os.chdir(cwd)


    os.chdir(origin)

def print_images(origin,path)
    path_b = '\\images\\osprey_raw.jpg'
    path_c = '\\images\\cathedral_raw.jpg'
    path_d = '\\images\\ocean_birds_raw.jpg'
    path_e = '\\images\\tropicalfish.jpg'
    path_f = '\\images\\SteeringWheel_raw.jpg'

    paths = [path_b, path_c, path_d, path_e, path_f]

    thresholds = (16,1500)

    trees_man = []
    trees_var = []

    for path in paths:
        path_temp = path
        path = origin + path
        #load in an image to test
        image = cv.imread(path)

        height, width, channels = image.shape
        pixels = height * width

        original_image = plt.imread(path)

        height, width, channels = image.shape
        pixels = height * width

        #measure the time to build using the Manhattan Metric
        start = time.time()
        quad_manhattan = qt.Quadtree(image,thresholds[0],'Manhattan','quad')
        end = time.time()-start
        count_man = quad_manhattan.nodecount()

        #measure the time to build using the                                              
        start2 = time.time()
        quad_variance  = qt.Quadtree(image,thresholds[1],'Variance','quad')
        end2 = time.time()-start
        count_var = quad_variance.nodecount()

        print "The manahattan splitting criterion took " + str(end) + " seconds to build."
        print "It reduced to image from "+ str(pixels) + " pixels down to " + str(count_man) + " nodes"
        print "Reducing the size by a factor of " + str(pixels/count_man) + "\n"


        print "The variance splitting criterion took " + str(end2) + " seconds to build."
        print "It reduced to image from "+ str(pixels) + " pixels down to " + str(count_var) + " nodes"
        print "Reducing the size by a factor of " + str(pixels/count_var) 


        output_man = quad_manhattan.toimage(quad_manhattan.RootNode, mode = "smooth")
        output_var = quad_variance.toimage( quad_variance.RootNode , mode = "smooth")

        path_man = "Manhattan" + path_temp[9:] + ".jpg"
        path_var = "Variance"  + path_temp[9:] +".jpg"

        cv.imwrite(origin + "\\" + path_man, output_man)
        cv.imwrite(origin + "\\" + path_var, output_var)

        imcompare(path_man,path_var,"Manhattan","Variance")

        trees_man.append(quad_manhattan)
        trees_var.append(quad_variance)

def tree_display()
    for i in range(len(trees_man)/2):
        path_temp = "treeman" + str(i)
        path = origin + path_temp
        #load in an image to test
        quad2 = trees_man[i] 
        if quad2.toMatrix():
            m_path =  "morph" + path_temp + ".jpg"
            mpath2 =  "opening" + path_temp + ".jpg"
            
            cv.imwrite(origin + "\\"+ m_path,quad2.Matrix)
            cv.imwrite(origin + "\\" + mpath2,quad2.Opening)
        
        imcompare(m_path,mpath2,"Nodes","Morphological operation")


def tree_makes():
manhattan = range(8,33,8) 
variance  = range(400,1001,200)

thresholds = zip(manhattan,variance)


path = origin+'\\images\\redbugs_raw.jpg'

#load in an image to test
image = cv.imread(path)

original_image = plt.imread(path)

plt.figure(figsize = (30,24))
plt.imshow(original_image)
plt.title("original image")
plt.show()

height, width, channels = image.shape
pixels = height * width

#for each step up the threshold compare the compression rate, time to build, and final image
for threshold in thresholds:
    
    #measure the time to build using the Manhattan Metric
    start = time.time()
    quad_manhattan = qt.Quadtree(image,threshold[0],'Manhattan','quad')
    end = time.time()-start
    count_man = quad_manhattan.nodecount()
    
    #measure the time to build using the                                              
    start2 = time.time()
    quad_variance  = qt.Quadtree(image,threshold[1],'Variance','quad')
    end2 = time.time()-start
    count_var = quad_variance.nodecount()
                      
    print "The manahattan splitting criterion took " + str(end) + " seconds to build."
    print "It reduced to image from "+ str(pixels) + " pixels down to " + str(count_man) + "nodes"
    print "Reducing the size by a factor of " + str(pixels/count_man) + "\n"
    
    
    print "The variance splitting criterion took " + str(end2) + " seconds to build."
    print "It reduced to image from "+ str(pixels) + " pixels down to " + str(count_var) + " nodes"
    print "Reducing the size by a factor of " + str(pixels/count_var) 
    
    
    output_man = quad_manhattan.toimage(quad_manhattan.RootNode, mode = "smooth")
    output_var = quad_variance.toimage( quad_variance.RootNode , mode = "smooth")
    
    path_man = "Manhattan"+str(threshold[0])+".jpg"
    path_var = "Variance"+str(threshold[1])+".jpg"
    cv.imwrite(origin + "\\" + path_man, output_man)
    cv.imwrite(origin + "\\" + path_var, output_var)
    
    imcompare(path_man,path_var,"Manhattan","Variance")
    