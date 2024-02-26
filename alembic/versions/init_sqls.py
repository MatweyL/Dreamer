init_task_data_template_data = """
INSERT INTO public.task_data_template
(task_type_uid, field_name, is_input, field_type, is_list, load_timestamp)
VALUES('00008888-5157-45e3-a6c0-0901d6c292a0'::uuid, 'internal_url', true, 'STRING'::public."fieldtypes", false, '2024-02-26 21:25:00.000');
INSERT INTO public.task_data_template
(task_type_uid, field_name, is_input, field_type, is_list, load_timestamp)
VALUES('11118888-5157-45e3-a6c0-0901d6c292a0'::uuid, 'text_size', true, 'INT'::public."fieldtypes", false, '2024-02-26 21:25:00.000');
INSERT INTO public.task_data_template
(task_type_uid, field_name, is_input, field_type, is_list, load_timestamp)
VALUES('22228888-5157-45e3-a6c0-0901d6c292a0'::uuid, 'style', true, 'STRING'::public."fieldtypes", false, '2024-02-26 21:25:00.000');
INSERT INTO public.task_data_template
(task_type_uid, field_name, is_input, field_type, is_list, load_timestamp)
VALUES('00008888-5157-45e3-a6c0-0901d6c292a0'::uuid, 'internal_url', false, 'STRING'::public."fieldtypes", false, '2024-02-26 21:25:00.000');
INSERT INTO public.task_data_template
(task_type_uid, field_name, is_input, field_type, is_list, load_timestamp)
VALUES('11118888-5157-45e3-a6c0-0901d6c292a0'::uuid, 'text', false, 'STRING'::public."fieldtypes", false, '2024-02-26 21:25:00.000');
INSERT INTO public.task_data_template
(task_type_uid, field_name, is_input, field_type, is_list, load_timestamp)
VALUES('22228888-5157-45e3-a6c0-0901d6c292a0'::uuid, 'internal_urls', false, 'STRING'::public."fieldtypes", true, '2024-02-26 21:25:00.000');
"""
init_pipeline_step_template_data = """
INSERT INTO public.pipeline_step_template
(pipeline_uid, previous_task_type_uid, current_task_type_uid, load_timestamp)
VALUES('88884444-5157-45e3-a6c0-0901d6c292a0'::uuid, NULL, '00008888-5157-45e3-a6c0-0901d6c292a0'::uuid, '2024-02-26 21:25:00.000');
INSERT INTO public.pipeline_step_template
(pipeline_uid, previous_task_type_uid, current_task_type_uid, load_timestamp)
VALUES('88884444-5157-45e3-a6c0-0901d6c292a0'::uuid, '00008888-5157-45e3-a6c0-0901d6c292a0'::uuid, '11118888-5157-45e3-a6c0-0901d6c292a0'::uuid, '2024-02-26 21:25:00.000');
INSERT INTO public.pipeline_step_template
(pipeline_uid, previous_task_type_uid, current_task_type_uid, load_timestamp)
VALUES('88884444-5157-45e3-a6c0-0901d6c292a0'::uuid, '11118888-5157-45e3-a6c0-0901d6c292a0'::uuid, '22228888-5157-45e3-a6c0-0901d6c292a0'::uuid, '2024-02-26 21:25:00.000');
"""
init_pipeline_data = """
INSERT INTO public.pipeline
("name", uid, load_timestamp)
VALUES('Image generation pipeline', '88884444-5157-45e3-a6c0-0901d6c292a0'::uuid, '2024-02-26 21:25:00.000');
"""