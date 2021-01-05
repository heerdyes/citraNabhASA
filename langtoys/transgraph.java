import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.HashMap;
import java.util.ArrayList;
import java.io.FileWriter;
import java.io.PrintWriter;

public class transgraph{
  static List<String> stmts=new ArrayList<String>();
  static HashMap<String,String> symtab=new HashMap<String,String>();
  
  static void d(String msg){
    System.out.println(msg);
  }
  
  static void f(String msg){
    System.out.println("[ERROR] "+msg);
    System.exit(0);
  }
  
  static void u(){
    d("usage: java transgraph <genartfile>");
    System.exit(0);
  }
  
  static void rendercode(String tmplfn,String outfn,String clsnm){
    try(
      FileWriter fw=new FileWriter(outfn);
      PrintWriter pw=new PrintWriter(fw);
    ){
      List<String> tlns=Files.readAllLines(Paths.get(tmplfn));
      for(String ln:tlns){
        if(ln.contains("#[clsnm]")){
          pw.printf("%s\n",ln.replace("#[clsnm]",clsnm));
        }else if(ln.contains("#[genart]")){
          int iloc=ln.indexOf("#[genart]");
          String prespace=ln.substring(0,iloc);
          for(String stmt:stmts){
            pw.printf("%s%s\n",prespace,stmt);
          }
        }else{
          pw.println(ln);
        }
      }
    }catch(Exception e){
      e.printStackTrace();
    }
  }
  
  static void transmuteline(String ln){
    String line=ln.strip();
    String car,cdr;
    if(line.contains(" ")){
      int ispc=line.indexOf(" ");
      car=line.substring(0,ispc);
      cdr=line.substring(ispc+1);
    }else{
      car=line;
      cdr="";
    }
    // no-ops
    if(line.length()==0) return;
    if(line.startsWith("#")) return;
    // commands
    if(car.equals("print")){
      String jgen=String.format("System.out.println(%s);",cdr);
      stmts.add(jgen);
    }else if(car.equals("let")){
      String[] args=cdr.split(" ");
      // validate let syntax
      if(!args[1].equals("be")){
        String exmsg=String.format("let statement syntax violated. found '%s' instead of 'be'",args[1]);
        throw new RuntimeException(exmsg);
      }
      String vnm=args[0];
      String vval=args[2];
      String jgen=String.format("var %s=%s;",vnm,vval);
      stmts.add(jgen);
    }else if(car.equals("line")){
      String[] args=cdr.split(" ");
      String jgen=String.format("gc.strokeLine(%s,%s,%s,%s);",args[0],args[1],args[2],args[3]);
      stmts.add(jgen);
    }else if(car.equals("inc")){
      String[] args=cdr.split(" ");
      stmts.add(String.format("%s+=%s;",args[0],args[1]));
    }else if(car.equals("end")){
      stmts.add("}");
    }else if(car.equals("repeat")){
      String[] args=cdr.split(" ");
      if(!args[1].equals("times")){
        throw new RuntimeException(
          String.format("[error] '%s' found instead of 'times'",args[1]));
      }
      try{
        Integer.parseInt(args[0]);
      }catch(NumberFormatException nfe){
        throw new RuntimeException("repeat command accepts only integers!");
      }
      String jgen=String.format("for(int i=0;i<%s;i++){",args[0]);
      stmts.add(jgen);
    }
  }
  
  public static void main(String[] args){
    if(args.length!=1) { u(); }
    d(args[0]);
    try{
      String fn=args[0];
      String[] nmext=fn.split("\\.");
      String clsnm=nmext[0];
      String gaext=nmext[1];
      if(!gaext.equals("ga")){
        d("genartfile must have extension .ga!");
      }
      List<String> lines=Files.readAllLines(Paths.get(fn));
      for(String ln:lines){
        transmuteline(ln);
      }
      rendercode("FXTemplate.java","zero.java","zero");
    }catch(IOException e){
      e.printStackTrace();
    }
  }
  
}
