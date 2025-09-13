import java.io.*;
import java.util.*;

public class checker{ 

    private static Set<String>usedwords = new HashSet<>();

    static{ 
        try(BufferedReader br = new BufferedReader(new FileReader("list.txt"))){ 
            String line; 
            while((line = br.readLine()) != null){ 
                usedwords.add(line.trim().toLowerCase()); 
            }    
        }
        catch(IOException e){ 
            System.out.println("Couldn't fid the list!!!");
        }
    }
    public static String check(String password){ 
        if(usedwords.contains(password.toLowerCase())){ 
            return "Commonly used password!";
        }
        int score = 0; 
        StringBuilder feedback = new StringBuilder("Missing: ");

        int pwd_length = password.length(); 
        if (password.length() >= 8){ 
            score++;
        } 
        else{ 
            feedback.append("at least 8 characters, ");
        }

        if (password.matches(".*[A-Z].*")){
            score++;
        } 
        else{ 
            feedback.append("uppercase letter, ");
        } 
        if (password.matches(".*[a-z].*")){ 
            score++;
        } 
        else{ 
            feedback.append("lowercase letter, ");
        } 
        if (password.matches(".*\\d.*")){ 
            score++;
        }
        else{ 
            feedback.append("number, ");}

        if (password.matches(".*[@$!%*?&].*")){ 
            score++;} 
        else{ 
            feedback.append("special character (@$!%*?&), ");
        } 

        if(feedback.toString().endsWith(", ")){ 
            feedback.setLength(feedback.length() - 2); 
        }
        if(score <= 2){ 
            return "Weak Password! " + feedback; 
        }
        else if (score == 3 || score == 4) { 
            return "Medium Password! " + feedback; 
        }
        else{ 
                return "Strong Password! Nice Going!";
            }
        }

    public static void main(String[] args){ 
        Scanner sc = new Scanner(System.in); 
        System.out.print("Enter password: "); 
        String password = sc.nextLine(); 

        String strength = check(password); 
        System.out.println(strength);
    }
        
    }
