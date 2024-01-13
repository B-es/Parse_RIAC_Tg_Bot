#encoding "utf8"

PersonSurname -> Word<GU=[sg,nom]|&[sg,gen]|&[sg,dat]|&[sg,acc]|&[sg,ins]|&[sg,loc]|&[sg,abl]|&[sg,voc],kwtype="фамилия">;

PersonName -> Word<GU=[sg,nom]|&[sg,gen]|&[sg,dat]|&[sg,acc]|&[sg,ins]|&[sg,loc]|&[sg,abl]|&[sg,voc],kwtype="имя">;

AttractionName -> AnyWord<GU=[sg,nom]|&[sg,gen]|&[sg,dat]|&[sg,acc]|&[sg,ins]|&[sg,loc]|&[sg,abl]|&[sg,voc],kwtype="название">;

PersonN -> PersonName interp (Person.Name);
PersonS -> PersonSurname interp (Person.Surname);
NameAttraction -> AttractionName interp (NameAttraction.Name); 
Person -> PersonN PersonS | PersonS PersonN;
Person -> NameAttraction;

