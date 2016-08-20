function GenBeanUtils() {
	// Config Posible Datatype
    this.allDataTypes = new Array(
	"java.lang.String",
	"java.lang.Boolean",
	"java.lang.Integer",
	"java.math.BigDecimal",
	"java.lang.Long",
	"java.lang.Double",
	"java.lang.Short",
	"java.lang.Byte[]",
	"java.lang.Real",
	"java.lang.Byte",
	"java.lang.Object",
	"java.util.Date",
	"th.co.cdgs.lov.LovState",
	"java.util.List<\?>",
	"somepackage.Enum\?");
	
	//Config Posible Datatype require import
	this.importType = new Array("java.math.BigDecimal","java.util.Date","th.co.cdgs.lov.LovState","th.co.cdgs.validator.constaints.LovRequired","org.hibernate.validator.constraints.NotBlank","javax.validation.constraints.NotNull","org.hibernate.validator.constraints.NotEmpty");
	
	
    var javaTypeToSimpleType = function(typeName)   // Only visible inside GenBeanUtils()
    {
        return typeName.substring(typeName.lastIndexOf('.')+1);
    }
	
	var attrToFunctionName = function(attrName){
		return attrName.substring(0,1).toUpperCase()+attrName.substring(1);
	}
	
	this.getTypeByIndex = function(index)   // getAllSimpleType is visible to all
    {
       return this.allDataTypes[index];
    }
	
	this.getSimpleTypeByIndex = function(index)   // getAllSimpleType is visible to all
    {
       return javaTypeToSimpleType(this.allDataTypes[index]);
    }
	
	this.getAllSimpleType = function()   // getAllSimpleType is visible to all
    {
        var types = new Array();
		this.allDataTypes.forEach(function(type) {
			types.push(javaTypeToSimpleType(type));
		});
		//alert(types);
		return types;
    }
	
	this.isImportType = function(type){
		return $.inArray(type, this.importType) != -1;
	}
	
	this.toMethodGet = function(simpletype,attrName){
		var methodStr = "\tpublic "+simpletype+" get"+attrToFunctionName(attrName)+"() {\n"
					 + "\t\treturn this."+attrName+";\n"
					 + "\t}\n\n";
		return methodStr;
	}
	
	this.toMethodSet = function(simpletype,attrName){
		var methodStr = "\tpublic void set"+attrToFunctionName(attrName)+"("+simpletype+" "+attrName+") {\n"
					 + "\t\tthis."+attrName+" = "+attrName+";\n"
					 + "\t}\n\n";
		return methodStr;
	}
	
	this.cutJavaPackage = function(typeName)  
    {
        return typeName.substring(typeName.lastIndexOf('.')+1);
    }
}