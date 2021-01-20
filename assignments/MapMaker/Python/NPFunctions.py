import numpy as np
# Numpy Helper Functions
# Take a single position from provided path file and convert it to a numpy array 
def conv_pos_to_np(pos):
    return np.array([pos["X"], pos["Y"], pos["Z"]])

def conv_pos_to_np_path_matrix(pos):
    return conv_pos_to_np(pos).reshape(1,3)

# Take a path from provided path files and convert it to a numpy array
def conv_path_to_np(p):
    return np.array(  [ conv_pos_to_np(pos) for pos in p  ])

def compute_distances_vector_matrix(robot_pos, path_matr):
        """ Get the distances between Xtrain and Zpredict
        Note:
            1. Optimization level - highly optimized!
            
            Algorithm was found https://medium.com/@souravdey/l2-distance-matrix-vectorization-trick-26aa3247ac6c
            It is a no loop solution, which means it can handle the matrices in
            one line of code rather than having to iterate over the rows of one
            matrix
            
            2. I have removed the square root to further optimize the calculation.
            This is ok, because I do not need the actual distance between points. 
            I just need a list of the relative distances. Since the sq root is 
            monotonic, it preserverses the order.         
        """
        # Convert position vector into a matrix
        robot_pos_matr = np.full(path_matr.shape,robot_pos)

        #print("robot_pos_matr",robot_pos_matr.shape,robot_pos_matr)
        dists = np.sqrt(-2 * np.dot(path_matr, robot_pos_matr.T) + np.sum(robot_pos_matr**2, axis=1) + np.sum(path_matr**2, axis=1)[:, np.newaxis])
        #dists = -2 * np.dot(path_matr, robot_pos_matr.T) + np.sum(robot_pos_matr**2, axis=1) + np.sum(path_matr**2, axis=1)[:, np.newaxis]
        return dists[:,0]