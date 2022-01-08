# /**
#  * @author jateengandhi
#  * @email 
#  * @create date 2021-05-14 14:58:28
#  * @modify date 2021-05-14 14:58:28
#  * @desc [description]

## This program utilizes two methods to check 
# 	if an array is a magic square of any size
# 	that satisfies the following conditions:
# 1. Square 2D array
# 2. Elements are integers in the range 1, 2, ..., size of array
# 3. Sums of all rows, columns, and both diagonals are identical
 
 
# Method 1 uses class 2Dsquare to create an instance of a matrix 
#   from list of lists or tuple of tuples
 
# Method 2 utilizes python's numpy module to create a matrix
import numpy as np
 
# Custom error for catching square 2D array exception
class Not2DSquareException(Exception):
    '''Raised by 2DSquare and checkMatrix method
        if the matrix is either not 2D or not a square'''
    
    def __init__(self):
        self.statement = 'Array is not either 2D or square'
    
    def __str__(self):
        return self.statement
 
# Custom error for catching non-distinct elements exception
class NotDistinctException(Exception):
    '''Raised by 2DSquare and checkMatrix method
        if all of the elements are not 1, 2, ..., n'''
    
    def __init__(self):
        self.statement = 'Array does not have 1, 2, ..., n numbers'
 
    def __str__(self):
        return self.statement
 
# -----------------------------------------------------------------------------------
# METHOD 1:
class twoDSquare(object):
    '''Creates an instance of a 2D square matrix 
        from an array of list of lists or tuple of tuples
    2D array is flattened into a 1D list
    Rows, columns, and diagonals of the instance 
        are dictionaries whose keys are row/col numbers
        and values are lists of indexes identifying 
        elements in the flattened 1D list
    Useful when numpy module is 
        either not installed or not imported'''
    
    def __init__(self, arr):
        self.arr = arr
        self.lst =[]
    
        # Check for 2D array
        # 1st element of 1st list/tuple is an int
        if isinstance(self.arr[0][0], int):
            
            # Square test 
            # 	if number of lists is equal to element in each list
            if all([len(arr) == len(l) for l in arr]):

                # Append all lists/tuples into a single list
                for lst in self.arr:
                    self.lst += lst
 
            else:
                raise Not2DSquareException
        else:
            raise NotDistinctException

        
        # set() method finds and sorts unique elements
        self.sortedList = list(set(self.lst)) 
 
        # 1st element should be 1 and 
        # 	last should be n (no. of total elements)
        if self.sortedList[0] == 1 and \
            self.sortedList[-1] == len(self.lst):
            pass     
        
        else:
            # Elements are not distinct
            raise NotDistinctException
               
        # Keys of the rows dictionary are the row numbers
            # Value is a list of indexes for that row
        self.rows = {}
        
        for r in range(self.nRows()):
            
            # e.g. 0th row of 3x3 has indexes 0, 1, 2
            #   1st row has indexes 3, 4, 5
            self.rows[r] = [row  for row 
                    in range(r*self.nRows(), self.nRows()*(1+r))]
 
        # Keys of cols dictionary are column numbers
        # Value is the list of indexes for that column
        self.cols = {}
        
        for c in range(self.nCols()):
        
            # e.g. 0th column of 3x3 has indexes 0, 3, 6
            #   1st column has indexes 1, 4, 7
            self.cols[c] = [c+r for r in 
                    range(0, self.mtxSize(), self.nCols())]
 
        # Indexes for top-left to bottom-right diagonal
        self.diag1 = [n for n in 
            range(0, self.mtxSize(), self.nRows()+1)]
        
        # Indexes for top-right to bottom-left diagonal
        self.diag2 = [n for n in 
            range(self.nRows()-1, self.mtxSize()-1, self.nRows()-1)]
 
 
    def mtxSize(self):
        '''Returns total number of elements'''
        return len(self.lst)
 
    def nRows(self):
        '''Returns number of rows'''
        return len(self.arr[0])
    
    def nCols(self):
        '''Returns number of columns'''
        return len(self.arr[0])
 
    def mtxShape(self):
        '''Returns tuple (rows, columns)'''
        return (self.nRows(), self.nCols())
 
    def getRow(self, row):
        '''Assumes row is an integer
            Returns elements of the row'''
        return [self.lst[c] for c in self.rows[row]]
 
    def getCol(self, col):
        '''Assumes col is an integer
            Returns elements of the column'''
        return [self.lst[r] for r in self.cols[col]]
 
    def getDiagonal(self, diag = 1):
        '''Returns either first or second diagonal'''
        if diag == 1:
            return [self.lst[i] for i in self.diag1]
        else:
            return [self.lst[i] for i in self.diag2]
 
# Method to check magic square with twoDSquare matrix
def withoutNP(matrix):
    '''Assumes matrix is an instance of class twoDSquare
        Returns true if the matrix is a magic square'''
 
    # Create list of sums of rows
    row_sums = [sum(matrix.getRow(row)) 
                for row in range(matrix.nRows())]
 
    # Create list of sums of columns
    col_sums = [sum(matrix.getCol(col)) 
                for col in range(matrix.nCols())]
    
    # Check if sums for each row, column, and diagonal are identical
    if set(row_sums) == set(col_sums) and \
        sum(matrix.getDiagonal(1)) == sum(matrix.getDiagonal(2)):
 
        
        # Array has passed all of the tests
        # It is a magic square
        print('Array is a magic square')
        return True
 
    else:
        # One or more of the sums do not match
        print('Sums do not match')
        return False
 
# -----------------------------------------------------------------------------------
# METHOD 2:
 
# Method to check the array
def checkMatrix(matrix):
    '''Assumes matrix is a numpy array
        Checks for the following conditions:
        (1) 2D, (2) square, and (3) all elements are unique
        Returns true if all conditions are satisfied'''
    
    # Check for number of rows and columns
    # Stores as a tuple
    mtx_shape = np.shape(matrix)
 
    # len() = 2 indicates 2D array
    # Identical elements of tuple will indicate square matrix
    if len(mtx_shape) == 2 and \
        mtx_shape[0] == mtx_shape[1]:
 
        # numpy.flatten() creates a 1D array of all elements
        # set() method finds unique elements and 
        #   sorts in increasing order
        # Stored as a list for indexing
        elem_list = list(set(matrix.flatten()))
 
        # Check if the first and last elements of the list 
        #   are 1 and size of matrix, respectively
        if elem_list[0] == 1 and elem_list[-1] == matrix.size:
            return True
        else:
            raise NotDistinctException
    else:
        raise Not2DSquareException
 
# Method to check magic square using numpy
def withNP(matrix):
    '''Assumes matrix is a numpy array
        Used when numpy module can be imported
        Returns true if the matrix is a magic square'''
    
    # Create a copy of the matrix
    mtx_array = np.copy(matrix)
 
    try:       
        # Check if matrix is a 2D square array 
        # with 1, 2, ..., n elements
        if checkMatrix(mtx_array):
 
            # Check if sums of rows, 
            #   columns, and diagonals are identical
            
            # numpy.sum method with axis = 0, and 1
            #   performs column wise and row wise additions, respectively,
            #   and stores results in a list
            
            # Set method finds unique values of the list
            # diagonal() and fliplr.diagonal() yields 
            #   a list of elements of each diagonal
            
            if set(np.sum(mtx_array, axis=0)) == set(np.sum(mtx_array, axis=1)) \
                                            and \
                sum(mtx_array.diagonal()) == sum(np.fliplr(mtx_array).diagonal()):
 
                # All conditions are satisfied
                # Array is a magic square
                print('Array is a magic square')
                return True
            
            else:
                # One or more of of the sums do not match
                print('Sums do not match')
                return False
    # Catch the exceptions from matrix check
    except Exception as inst:
        print(inst)
        return False
 
# This method calls either of the above 2 methods, based on availability of numpy
def isMagicSquare(arr):
    '''Assumes arr is an array
        Checks if the array is a 2D magic square
        '''
    try:
        import numpy as np
        
        # Check if matrix is a numpy array
        if isinstance(arr, np.ndarray):
            
            # If passes, copy numpy array
            matrix = np.copy(arr)
    
        # If not a numpy array
        elif isinstance(arr, (list, tuple)):
           
            # create a numpy array
            matrix = np.array(arr)
        
        # Run method 2, using numpy, to test magic square
        return withNP(matrix)
 
    # In the event when numpy module is not available or 
    #   has not been imported
    except NameError or ImportError:
        
        try:
            # Create instance of 2Dsquare matrix
            matrix = twoDSquare(arr)
            
            # Runt method 1, without numpy, to check magic square
            return withoutNP(matrix)
 
        # If the array is not square or
        #  does not have distinct elements
        except Exception as inst:
            print(inst)
            return False
 
# -----------------------------------------------------------------------------------
# Test the code for 2 types of arrays
if __name__ == '__main__':
    
    # Magic square is a list of lists
    test_square1_list = [[2, 7, 6],
                        [9, 5, 1],
                        [4, 3, 8]]
 
    # Magic square is a tuple of tuples
    test_square1_tuple = ((2, 7, 6),
                        (9, 5, 1),
                        (4, 3, 8))
 
    # Test and store results of each matrix
    test_results = [isMagicSquare(arr) for arr in 
                    [test_square1_list, 
                        test_square1_tuple]]
 
    if all(test_results):
        print('All tests passed')
 
# -----------------------------------------------------------------------------------
# Additional tests
# Magic square is a numpy array
test_square1 = np.array([[2, 7, 6],
                [9, 5, 1],
                [4, 3, 8]])
 
# Elements do not add up to the same value
test_square1b = [[2, 7, 6],
                [9, 1, 5],
                [4, 3, 8]]
 
# Missing element
test_square1c = [[None, 7, 6],
                [9, 1, 5],
                [4, 3, 8]]
 
# Negative integer
test_square1d = [[-2, 7, 6],
                [9, 5, 1],
                [4, 3, 8]]
 
# Not a 2D array
test_square1e = [[7, 6],
                [9, 5, 1],
                [4, 3, 8]]
 
# 4X4 magic square
test_square2 = [[2, 7, 12, 13],
                [16, 9, 6, 3],
                [5, 4, 15, 10],
                [11, 14, 1, 8]]
 
# 2D square with matching sums but
# 	elements do not begin with 1.
test_square2b = [[2, 16, 15, 5],
                [13, 7, 8 , 10],
                [9, 11, 12, 6],
                [14, 4, 3, 17]]