#include <iostream>
using namespace std;


int main ()
{
    /* Three main tasks of this project:
        1 - Expression Solving
        2 - Decisions Making(If-else structure)
        3 - Repetition Structure(while loop)
    */

    // Declaring Varibles .
    int x = 2,y = 1,z = 0, last_digit_of_student_vu_id = 0, sum_of_z_and_ID_digit = 0 ;
    string  student_vu_id = "BC200415506", student_name = "AHMED HASSAN YASEEN";

    
    // 1 - Expression Solving (Has performed).
    // Expression :  z = x² + 2xy - x/y .
    z = x*x + 2*x*y - (x/y) ; 
    cout <<"After evaluation of given expression the value of z = " << z <<endl;
    
    // Setting student VU id.
    char student_vu_id_array[] = "BC200415506" ;
  	int i;
  	for( i=0; i<student_vu_id.length(); i++)
  	{
    	// cout << student_vu_id_array[i];
  	}

    int j;
    char last_digit;
  	for( i=0; i<student_vu_id.length(); i++)
  	{
        if (i == student_vu_id.length()-1){
            last_digit=student_vu_id_array[i];
    	    // cout <<"did i got something"<< last_digit;
        }   
  	}

    // // Coverting Char into integer by cascading.
    last_digit_of_student_vu_id = last_digit - 48;//student_vu_id.back() - 48 ; 
    cout <<"Last digit of your VU id is = "<< last_digit_of_student_vu_id<<endl;

    //Adding/Summing value of Z and the last digit of vu ID.
    sum_of_z_and_ID_digit = z + last_digit_of_student_vu_id;

    // 2 - Decisions Making(If-else structure) (Performed below).
    if (sum_of_z_and_ID_digit%2!=0){
        cout <<"You got an odd number = "<<sum_of_z_and_ID_digit<<endl;

        // 3 - Repetition Structure(while loop)  (Has been performed below).
        int i=0;
        while (i<=sum_of_z_and_ID_digit){
            cout<<"Iteration: "<<i<<endl;
            cout<<"Your VU ID is "<<student_vu_id<<endl ;
            i++;
        };

        cout<<endl<<"****    Thank you for testing!     ****\n\n";

    } else if (sum_of_z_and_ID_digit%2==0){
        cout <<"You got an even number = "<<sum_of_z_and_ID_digit<<endl;

        // 3 - Repetition Structure(while loop)  (Has been performed below).
        int i=0;
        while (i<=sum_of_z_and_ID_digit){
            cout<<"Iteration: "<<i<<endl;
            cout<<"My name is "<<student_name<<endl ;
            i++;
        };

        cout<<endl<<"****    Thank you for testing!     ****\n\n";

    } else {
        cout <<"Invalid student credentials.";
    };
}