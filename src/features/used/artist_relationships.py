"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""
from src.utils.decorator_annotations import annotations
from src.features.decorator_timing_feature import timing_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
import musicbrainzngs


@annotations({'edge_types': ['cc9fcb45-7ab5-4629-bc5f-277f2592fa5a', 'a255bca1-b157-4518-9108-7b147dc3fc68', 'd59d99ea-23d4-4a80-b066-edca32ee158f', '3e48faba-ec01-47fd-8e89-30e81161661c', '7474ab81-486f-40b5-8685-3a4f8ea624cb', 'eeb9c319-9fde-4313-b76d-29db1576aad8', 'da6c5d8a-ce13-474d-9375-61feb29039a5', 'cb887d1b-5267-4f3d-badb-5b3fba7349f6', 'd3fd781c-5894-47e2-8c12-86cc0e2c8d08', '0084e70a-873e-4f7f-b3ff-635b9e863dae', '0a1771e1-8639-4740-8a43-bdafc050c3da', '6a88b92b-8fb5-41b3-aa1f-169ee7e05ed6', '7d166271-99c7-3a13-ae96-d2aab758029d', '95f0213a-dbe0-4d36-8036-9782e425e98a', '26131498-00e8-4136-b937-22a4be01a63d', '5cc8cfb5-cca0-4395-a44b-b7d3c1777608', '7231dcac-d2dc-4b4a-b218-ecea4123a4cd', 'a442b140-830b-30b0-a4aa-2e36f098b6aa', '535fdfed-3bca-40ad-966b-e67be7882d09', '936c7c95-3156-3889-a062-8a0cd57f8946', '492a850e-97eb-306a-a85e-4b6d98527796', '292df906-98a6-307e-86e8-df01a579a321', '76e8523e-567c-3e44-a302-3c75e601fcc2', '9b2d5b96-b4d9-4bce-b056-c369ced25e81', '92873f0d-12a7-4fb3-9eac-ff06c38c6a60', 'e5e6a204-8f81-4b17-9b54-a73a1a6db2bb', '2c5c92da-259c-42fc-ac1f-53d9dda2d6d0', '9da4b1cc-cdfa-425d-b5bc-83222046c805', '4ef86173-7f40-486d-bf8d-c38b1097e77f', 'e74a40e7-0f27-4e05-bdbd-eb10f5309472', '577996f3-7ff9-45cf-877e-740fb1267a63', '46981330-d73c-4ba5-845f-47f467072cf8', '5f9374d2-a0fa-4958-8a6f-80ca67e4aaa5', '85d1947c-1986-42f0-947c-80aab72a548f', 'b336d682-592f-4486-9f45-3d5d59895bdc', 'fe16f2bd-d324-435a-8076-bcf43b805bd9', '8fecc8a7-0df7-4637-9152-f12a07f0e9cd', '92859e2a-f2e5-45fa-a680-3f62ba0beccc', '5be4c609-9afa-4ea0-910b-12ffb71e3821', '7802f96b-d995-4ce9-8f70-6366faad758e', 'ab666dde-bd85-4ac2-a209-165eaf4146a0', 'cac01ac7-4159-42fd-9f2b-c5a7a5624079', '6ed4bfc4-0a0d-44c0-b025-b7fc4d900b67', '88562a60-2550-48f0-8e8e-f54d95c7369a', '610d39a4-3fa0-4848-a8c9-f46d7b5cc02e', 'ed6a7891-ce70-4e08-9839-1f2f62270497', 'a6f62641-2f58-470e-b02b-88d7b984dc9f', 'e259a3f5-ce8e-45c1-9ef7-90ff7d0c7589', '75c09861-6857-4ec0-9729-84eefde7fc86', 'dd9886f2-1dfe-4270-97db-283f6839a666', '249fc24f-d573-4290-9d74-0547712d1f1e', '094b1ddf-3df3-4fb9-8b01-cfd28e45da80', 'e794f8ff-b77b-4dfe-86ca-83197146ef10', '9421ca84-934f-49fe-9e66-dea242430406', 'b42b7966-b904-449e-b8f9-8c7297b863d0', 'b2bf7a5d-2da6-4742-baf4-e38d8a7ad029', 'fd3927ba-fd51-4fa9-bcc2-e83637896fe8', '1af24726-5b1f-4b07-826e-5351723f504b', '666c5ee3-b763-4b74-8f71-3456dfd3e755', '350f7ab7-c2d9-4f00-98e0-e1973bf4a2bf', '67ed1d31-8993-442c-aa59-afdb6a89d2c2', '98e2ad89-6641-4336-913d-db1515aaabcb', 'fff4640a-0819-49e9-92c5-1e3b5134fd95', '54fcf574-eb3a-40da-839f-986d46997b97', '7f7d829b-6ba8-4f86-be90-c9372ef9a679', 'cad0dbab-c711-442a-a91c-05359f0228ce', '72854c7e-ebf8-4b73-9b2c-ee08e83b9480', '24fce292-8a25-4039-b313-611a3678a42a', '58e18f90-fb7d-41d8-a70d-8d750fb73617', '3e23fc35-10c3-4dc9-a4f5-e3803643d5c1', '8a3994fd-71ec-4443-9882-2192801241f2', 'f8673e29-02a5-47b7-af61-dd4519328dd0', '628a9658-f54c-4142-b0c0-95f031b544da', '59054b12-01ac-43ee-a618-285fd397e461', '0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa', '3b6616c5-88ba-4341-b4ee-81ce1e6d7ebb', '234670ce-5f22-4fd0-921b-ef1662695c5d', '45115945-597e-4cb9-852f-4e6ba583fcc8', 'ffeaa74f-8295-45ee-a2f2-7c0cc1f73b1e', '22661fb8-cdb7-4f67-8385-b2a8be6c9f0d', '4820daa1-98d6-4f8b-aa4b-6895c5b79b27', '38fa7405-f9a5-48cb-827a-8ac601933ba0', '8a2799e8-a7e2-41ce-a7da-b5f520687216', '91109adb-a5a3-47b1-99bf-06f88130e875', '35ba2b3b-aaeb-4db1-bc5f-f42154e785d8', '28338ee6-d578-485a-bb53-61dbfd7c6545', '7950be4d-13a3-48e7-906b-5af562e39544', '83f72956-2007-4bca-8a97-0ae539cca99d', '1ef6f500-d098-4768-ad00-72cc2bc2912f', '601fc03e-1058-4ee6-a546-b914d55aa6ba', '578ee04d-3227-4335-ba2c-11e8ba420e0b', 'b367fae0-c4b0-48b9-a40c-f3ae4c02cffc', '5c0ceac3-feb4-41f0-868d-dc06f6e27fc0', '5dcc52af-7064-4051-8d62-7d80f4c3c907', 'ca8d6d99-b847-439c-b0ec-33d8a1b942bc', '30adb2d7-dbcc-4393-9230-2098510ce3c1', '0cd6aa63-c297-42ed-8725-c16d31913a98', '3e3102e1-1896-4f50-b5b2-dd9824e46efe', 'a01ee869-80a8-45ef-9447-c59e91aa7926', '36c50022-44e0-488d-994b-33f11d20301e', '40dff87a-e475-4aa6-b615-9935b564d756', '0748fa55-56b5-4ad5-8ce8-15b97f82a0c2', '68330a36-44cf-4fa2-84e8-533c6fe3fc23', '75e37b65-7b50-4080-bf04-8c59c66b5f65', '7fd5fbc0-fbf4-4d04-be23-417d50a4dc30', 'b1edc6f6-283d-4e32-b625-b96cfb192056', '8dc10cef-3116-4b3d-8e3e-33ffb84a97df', '0eb67a3e-796b-4394-ab6e-1224f43236b6', '9aae9a3d-7cc2-4eee-881d-b8b73d0ceef3', '4af8e696-2690-486f-87db-bc8ec2bfe859', '38751410-ee52-435b-af75-957cb4c34149', 'a7e408a1-8c64-4122-9ec2-906068955187', 'acad5736-9426-4b97-a660-33a5f8e83b28', '9ef2ba0d-953c-43a9-b1b5-cf2ba5986406', '8db9d0b7-ca39-43a6-8c72-9a47f811229e', '888a2320-52e4-4fe8-a8a0-7a4c8dfde167', '67555849-61e5-455b-96e3-29733f0115f5', 'eb10f8a0-0f4c-4dce-aa47-87bcb2bc42f3', '23a2e2e7-81ca-4865-8d05-2243848a77bf', '9ae9e4d0-f26b-42fb-ab5c-1149a47cf83b', 'b9129850-73ec-4af5-803c-1c12b97e25d2', '8a2b1c46-0fe5-42f7-9d72-f68604244c1d', 'd6b8f1d2-5431-4c97-9688-44f73213ee5b', '2f81887a-8674-4d8b-bd48-8bfd4c6fa332', '9162dedd-790c-446c-838e-240f877dbfe2', 'ac6a86db-f757-4815-a07e-744428d2382b', '7ddb04ae-6c8a-41bd-95c2-392994d663db', '800a8a16-5426-4f4e-8dd6-9371d8bc8398', 'ca7a474a-a1cd-4431-9230-56a17f553090', '01ce32b0-d873-4baa-8025-714b45c0c754', 'a2af367a-b040-46f8-af21-310f92dfe97b', 'dd182715-ca2b-4e4b-80b1-d21742fda0dc', '4db37fec-eb67-45d3-b4fa-148a68135fbb', '34d5334e-a4c8-4b65-a5f8-bbcc9c81d13d', '18f159bb-44f0-4aef-b198-a4736ad9b659', '04e1f0b6-ef40-4168-ba25-42a87729fe09', 'd7d9128d-e676-4d8f-a353-f48a55a98501', '3172a175-7c9d-44ce-a8b7-9a9187b33762', '8bf377ba-8d71-4ecc-97f2-7bb2d8a2a75f', '87e922ba-872e-418a-9f41-0a63aa3c30cc', 'b04848d7-dbd9-4be0-9d8c-13df6d6e40db', '84453d28-c3e8-4864-9aae-25aa968bcf9e', '904e57f3-cbbc-43ab-8798-13e710e400d3', '271306ca-c77f-4fe0-94bc-dd4b87ae0205', '6cc958c0-533b-4540-a281-058fbb941890', '023a6c6d-80af-4f88-ae69-f5f6213f9bf4', '617063ad-dbb5-4877-9ba0-ba2b9198d5a7', 'f30c29d3-a3f1-420d-9b6c-a750fd6bc2aa', '97169e5e-c978-486e-a5ea-da353ca9ea42', '0b63af5e-85b2-4891-8234-bddab251399d', '730b5251-7432-4896-8fc6-e1cba943bfe1', '01d3488d-8d2a-4cff-9226-5250404db4dc', '1a900189-53ba-442a-9406-49c43ddecb3f', 'b0f98226-7121-4db5-a69c-552e6d061da2', 'f3b80a09-5ebf-4ad2-9c46-3e6bce971d1b', '307e95dd-88b5-419b-8223-b146d4a0d439', '9c02ea37-7680-4fb5-8555-e330c7aa885b', 'cf43b79e-3299-4b0c-9244-59ea06337107', 'a6029157-d96b-4dc3-9f73-f99f76423d11', '74518a6b-589d-460e-8dd7-a8383851040a', '0b58dc9b-9c49-4b19-bb58-9c06d41c8fbf', '6ba2f0b3-90c5-471a-9bde-79d0612d023d', '7a573a01-8815-44db-8e30-693faa83fbfa', '01323b4f-7aba-410c-8c91-cb224b963a40', '5e2907db-49ec-4a48-9f11-dfb99d2603ff', 'b41e7530-cde4-459c-b8c5-dfef08fc8295', '25dd0db4-189f-436c-a610-aacb979f13e2', 'e035ac25-a2ff-48a6-9fb6-077692c67241', 'cee8e577-6fa6-4d77-abc0-35bce13c570e']})
@annotations({'edge_type_to_node_type':
              {'0084e70a-873e-4f7f-b3ff-635b9e863dae': 'work_musicbrainz_id',
               '01323b4f-7aba-410c-8c91-cb224b963a40': 'release_musicbrainz_id',
               '01ce32b0-d873-4baa-8025-714b45c0c754': 'release_musicbrainz_id',
               '01d3488d-8d2a-4cff-9226-5250404db4dc': 'release_musicbrainz_id',
               '023a6c6d-80af-4f88-ae69-f5f6213f9bf4': 'release_musicbrainz_id',
               '04e1f0b6-ef40-4168-ba25-42a87729fe09': 'release_musicbrainz_id',
               '0748fa55-56b5-4ad5-8ce8-15b97f82a0c2': 'recording_musicbrainz_id',
               '094b1ddf-3df3-4fb9-8b01-cfd28e45da80': 'artist_musicbrainz_id',
               '0a1771e1-8639-4740-8a43-bdafc050c3da': 'work_musicbrainz_id',
               '0b58dc9b-9c49-4b19-bb58-9c06d41c8fbf': 'release_musicbrainz_id',
               '0b63af5e-85b2-4891-8234-bddab251399d': 'release_musicbrainz_id',
               '0cd6aa63-c297-42ed-8725-c16d31913a98': 'recording_musicbrainz_id',
               '0eb67a3e-796b-4394-ab6e-1224f43236b6': 'recording_musicbrainz_id',
               '0fdbe3c6-7700-4a31-ae54-b53f06ae1cfa': 'recording_musicbrainz_id',
               '18f159bb-44f0-4aef-b198-a4736ad9b659': 'release_musicbrainz_id',
               '1a900189-53ba-442a-9406-49c43ddecb3f': 'release_musicbrainz_id',
               '1af24726-5b1f-4b07-826e-5351723f504b': 'artist_musicbrainz_id',
               '1ef6f500-d098-4768-ad00-72cc2bc2912f': 'recording_musicbrainz_id',
               '22661fb8-cdb7-4f67-8385-b2a8be6c9f0d': 'recording_musicbrainz_id',
               '234670ce-5f22-4fd0-921b-ef1662695c5d': 'recording_musicbrainz_id',
               '23a2e2e7-81ca-4865-8d05-2243848a77bf': 'release_musicbrainz_id',
               '249fc24f-d573-4290-9d74-0547712d1f1e': 'artist_musicbrainz_id',
               '24fce292-8a25-4039-b313-611a3678a42a': 'place_musicbrainz_id',
               '25dd0db4-189f-436c-a610-aacb979f13e2': 'release_group_musicbrainz_id',
               '26131498-00e8-4136-b937-22a4be01a63d': 'work_musicbrainz_id',
               '271306ca-c77f-4fe0-94bc-dd4b87ae0205': 'release_musicbrainz_id',
               '28338ee6-d578-485a-bb53-61dbfd7c6545': 'recording_musicbrainz_id',
               '292df906-98a6-307e-86e8-df01a579a321': 'event_musicbrainz_id',
               '2c5c92da-259c-42fc-ac1f-53d9dda2d6d0': 'event_musicbrainz_id',
               '2f81887a-8674-4d8b-bd48-8bfd4c6fa332': 'release_musicbrainz_id',
               '307e95dd-88b5-419b-8223-b146d4a0d439': 'release_musicbrainz_id',
               '30adb2d7-dbcc-4393-9230-2098510ce3c1': 'recording_musicbrainz_id',
               '3172a175-7c9d-44ce-a8b7-9a9187b33762': 'release_musicbrainz_id',
               '34d5334e-a4c8-4b65-a5f8-bbcc9c81d13d': 'release_musicbrainz_id',
               '350f7ab7-c2d9-4f00-98e0-e1973bf4a2bf': 'place_musicbrainz_id',
               '35ba2b3b-aaeb-4db1-bc5f-f42154e785d8': 'recording_musicbrainz_id',
               '36c50022-44e0-488d-994b-33f11d20301e': 'recording_musicbrainz_id',
               '38751410-ee52-435b-af75-957cb4c34149': 'recording_musicbrainz_id',
               '38fa7405-f9a5-48cb-827a-8ac601933ba0': 'recording_musicbrainz_id',
               '3b6616c5-88ba-4341-b4ee-81ce1e6d7ebb': 'recording_musicbrainz_id',
               '3e23fc35-10c3-4dc9-a4f5-e3803643d5c1': 'place_musicbrainz_id',
               '3e3102e1-1896-4f50-b5b2-dd9824e46efe': 'recording_musicbrainz_id',
               '3e48faba-ec01-47fd-8e89-30e81161661c': 'work_musicbrainz_id',
               '40dff87a-e475-4aa6-b615-9935b564d756': 'recording_musicbrainz_id',
               '45115945-597e-4cb9-852f-4e6ba583fcc8': 'recording_musicbrainz_id',
               '46981330-d73c-4ba5-845f-47f467072cf8': 'record_label_musicbrainz_id',
               '4820daa1-98d6-4f8b-aa4b-6895c5b79b27': 'recording_musicbrainz_id',
               '492a850e-97eb-306a-a85e-4b6d98527796': 'event_musicbrainz_id',
               '4af8e696-2690-486f-87db-bc8ec2bfe859': 'recording_musicbrainz_id',
               '4db37fec-eb67-45d3-b4fa-148a68135fbb': 'release_musicbrainz_id',
               '4ef86173-7f40-486d-bf8d-c38b1097e77f': 'event_musicbrainz_id',
               '535fdfed-3bca-40ad-966b-e67be7882d09': 'work_musicbrainz_id',
               '54fcf574-eb3a-40da-839f-986d46997b97': 'place_musicbrainz_id',
               '577996f3-7ff9-45cf-877e-740fb1267a63': 'record_label_musicbrainz_id',
               '578ee04d-3227-4335-ba2c-11e8ba420e0b': 'recording_musicbrainz_id',
               '58e18f90-fb7d-41d8-a70d-8d750fb73617': 'place_musicbrainz_id',
               '59054b12-01ac-43ee-a618-285fd397e461': 'recording_musicbrainz_id',
               '5be4c609-9afa-4ea0-910b-12ffb71e3821': 'artist_musicbrainz_id',
               '5c0ceac3-feb4-41f0-868d-dc06f6e27fc0': 'recording_musicbrainz_id',
               '5cc8cfb5-cca0-4395-a44b-b7d3c1777608': 'work_musicbrainz_id',
               '5dcc52af-7064-4051-8d62-7d80f4c3c907': 'recording_musicbrainz_id',
               '5e2907db-49ec-4a48-9f11-dfb99d2603ff': 'release_group_musicbrainz_id',
               '5f9374d2-a0fa-4958-8a6f-80ca67e4aaa5': 'record_label_musicbrainz_id',
               '601fc03e-1058-4ee6-a546-b914d55aa6ba': 'recording_musicbrainz_id',
               '610d39a4-3fa0-4848-a8c9-f46d7b5cc02e': 'artist_musicbrainz_id',
               '617063ad-dbb5-4877-9ba0-ba2b9198d5a7': 'release_musicbrainz_id',
               '628a9658-f54c-4142-b0c0-95f031b544da': 'recording_musicbrainz_id',
               '666c5ee3-b763-4b74-8f71-3456dfd3e755': 'place_musicbrainz_id',
               '67555849-61e5-455b-96e3-29733f0115f5': 'release_musicbrainz_id',
               '67ed1d31-8993-442c-aa59-afdb6a89d2c2': 'place_musicbrainz_id',
               '68330a36-44cf-4fa2-84e8-533c6fe3fc23': 'recording_musicbrainz_id',
               '6a88b92b-8fb5-41b3-aa1f-169ee7e05ed6': 'work_musicbrainz_id',
               '6ba2f0b3-90c5-471a-9bde-79d0612d023d': 'release_musicbrainz_id',
               '6cc958c0-533b-4540-a281-058fbb941890': 'release_musicbrainz_id',
               '6ed4bfc4-0a0d-44c0-b025-b7fc4d900b67': 'artist_musicbrainz_id',
               '7231dcac-d2dc-4b4a-b218-ecea4123a4cd': 'work_musicbrainz_id',
               '72854c7e-ebf8-4b73-9b2c-ee08e83b9480': 'place_musicbrainz_id',
               '730b5251-7432-4896-8fc6-e1cba943bfe1': 'release_musicbrainz_id',
               '74518a6b-589d-460e-8dd7-a8383851040a': 'release_musicbrainz_id',
               '7474ab81-486f-40b5-8685-3a4f8ea624cb': 'work_musicbrainz_id',
               '75c09861-6857-4ec0-9729-84eefde7fc86': 'artist_musicbrainz_id',
               '75e37b65-7b50-4080-bf04-8c59c66b5f65': 'recording_musicbrainz_id',
               '76e8523e-567c-3e44-a302-3c75e601fcc2': 'event_musicbrainz_id',
               '7802f96b-d995-4ce9-8f70-6366faad758e': 'artist_musicbrainz_id',
               '7950be4d-13a3-48e7-906b-5af562e39544': 'recording_musicbrainz_id',
               '7a573a01-8815-44db-8e30-693faa83fbfa': 'release_musicbrainz_id',
               '7d166271-99c7-3a13-ae96-d2aab758029d': 'work_musicbrainz_id',
               '7ddb04ae-6c8a-41bd-95c2-392994d663db': 'release_musicbrainz_id',
               '7f7d829b-6ba8-4f86-be90-c9372ef9a679': 'place_musicbrainz_id',
               '7fd5fbc0-fbf4-4d04-be23-417d50a4dc30': 'recording_musicbrainz_id',
               '800a8a16-5426-4f4e-8dd6-9371d8bc8398': 'release_musicbrainz_id',
               '83f72956-2007-4bca-8a97-0ae539cca99d': 'recording_musicbrainz_id',
               '84453d28-c3e8-4864-9aae-25aa968bcf9e': 'release_musicbrainz_id',
               '85d1947c-1986-42f0-947c-80aab72a548f': 'record_label_musicbrainz_id',
               '87e922ba-872e-418a-9f41-0a63aa3c30cc': 'release_musicbrainz_id',
               '88562a60-2550-48f0-8e8e-f54d95c7369a': 'artist_musicbrainz_id',
               '888a2320-52e4-4fe8-a8a0-7a4c8dfde167': 'release_musicbrainz_id',
               '8a2799e8-a7e2-41ce-a7da-b5f520687216': 'recording_musicbrainz_id',
               '8a2b1c46-0fe5-42f7-9d72-f68604244c1d': 'release_musicbrainz_id',
               '8a3994fd-71ec-4443-9882-2192801241f2': 'place_musicbrainz_id',
               '8bf377ba-8d71-4ecc-97f2-7bb2d8a2a75f': 'release_musicbrainz_id',
               '8db9d0b7-ca39-43a6-8c72-9a47f811229e': 'release_musicbrainz_id',
               '8dc10cef-3116-4b3d-8e3e-33ffb84a97df': 'recording_musicbrainz_id',
               '8fecc8a7-0df7-4637-9152-f12a07f0e9cd': 'record_label_musicbrainz_id',
               '904e57f3-cbbc-43ab-8798-13e710e400d3': 'release_musicbrainz_id',
               '91109adb-a5a3-47b1-99bf-06f88130e875': 'recording_musicbrainz_id',
               '9162dedd-790c-446c-838e-240f877dbfe2': 'release_musicbrainz_id',
               '92859e2a-f2e5-45fa-a680-3f62ba0beccc': 'artist_musicbrainz_id',
               '92873f0d-12a7-4fb3-9eac-ff06c38c6a60': 'event_musicbrainz_id',
               '936c7c95-3156-3889-a062-8a0cd57f8946': 'event_musicbrainz_id',
               '9421ca84-934f-49fe-9e66-dea242430406': 'artist_musicbrainz_id',
               '95f0213a-dbe0-4d36-8036-9782e425e98a': 'work_musicbrainz_id',
               '97169e5e-c978-486e-a5ea-da353ca9ea42': 'release_musicbrainz_id',
               '98e2ad89-6641-4336-913d-db1515aaabcb': 'place_musicbrainz_id',
               '9aae9a3d-7cc2-4eee-881d-b8b73d0ceef3': 'recording_musicbrainz_id',
               '9ae9e4d0-f26b-42fb-ab5c-1149a47cf83b': 'release_musicbrainz_id',
               '9b2d5b96-b4d9-4bce-b056-c369ced25e81': 'event_musicbrainz_id',
               '9c02ea37-7680-4fb5-8555-e330c7aa885b': 'release_musicbrainz_id',
               '9da4b1cc-cdfa-425d-b5bc-83222046c805': 'event_musicbrainz_id',
               '9ef2ba0d-953c-43a9-b1b5-cf2ba5986406': 'recording_musicbrainz_id',
               'a01ee869-80a8-45ef-9447-c59e91aa7926': 'recording_musicbrainz_id',
               'a255bca1-b157-4518-9108-7b147dc3fc68': 'work_musicbrainz_id',
               'a2af367a-b040-46f8-af21-310f92dfe97b': 'release_musicbrainz_id',
               'a442b140-830b-30b0-a4aa-2e36f098b6aa': 'work_musicbrainz_id',
               'a6029157-d96b-4dc3-9f73-f99f76423d11': 'release_musicbrainz_id',
               'a6f62641-2f58-470e-b02b-88d7b984dc9f': 'artist_musicbrainz_id',
               'a7e408a1-8c64-4122-9ec2-906068955187': 'recording_musicbrainz_id',
               'ab666dde-bd85-4ac2-a209-165eaf4146a0': 'artist_musicbrainz_id',
               'ac6a86db-f757-4815-a07e-744428d2382b': 'release_musicbrainz_id',
               'acad5736-9426-4b97-a660-33a5f8e83b28': 'recording_musicbrainz_id',
               'b04848d7-dbd9-4be0-9d8c-13df6d6e40db': 'release_musicbrainz_id',
               'b0f98226-7121-4db5-a69c-552e6d061da2': 'release_musicbrainz_id',
               'b1edc6f6-283d-4e32-b625-b96cfb192056': 'recording_musicbrainz_id',
               'b2bf7a5d-2da6-4742-baf4-e38d8a7ad029': 'artist_musicbrainz_id',
               'b336d682-592f-4486-9f45-3d5d59895bdc': 'record_label_musicbrainz_id',
               'b367fae0-c4b0-48b9-a40c-f3ae4c02cffc': 'recording_musicbrainz_id',
               'b41e7530-cde4-459c-b8c5-dfef08fc8295': 'release_group_musicbrainz_id',
               'b42b7966-b904-449e-b8f9-8c7297b863d0': 'artist_musicbrainz_id',
               'b9129850-73ec-4af5-803c-1c12b97e25d2': 'release_musicbrainz_id',
               'ca7a474a-a1cd-4431-9230-56a17f553090': 'release_musicbrainz_id',
               'ca8d6d99-b847-439c-b0ec-33d8a1b942bc': 'recording_musicbrainz_id',
               'cac01ac7-4159-42fd-9f2b-c5a7a5624079': 'artist_musicbrainz_id',
               'cad0dbab-c711-442a-a91c-05359f0228ce': 'place_musicbrainz_id',
               'cb887d1b-5267-4f3d-badb-5b3fba7349f6': 'work_musicbrainz_id',
               'cc9fcb45-7ab5-4629-bc5f-277f2592fa5a': 'work_musicbrainz_id',
               'cee8e577-6fa6-4d77-abc0-35bce13c570e': 'release_group_musicbrainz_id',
               'cf43b79e-3299-4b0c-9244-59ea06337107': 'release_musicbrainz_id',
               'd3fd781c-5894-47e2-8c12-86cc0e2c8d08': 'work_musicbrainz_id',
               'd59d99ea-23d4-4a80-b066-edca32ee158f': 'work_musicbrainz_id',
               'd6b8f1d2-5431-4c97-9688-44f73213ee5b': 'release_musicbrainz_id',
               'd7d9128d-e676-4d8f-a353-f48a55a98501': 'release_musicbrainz_id',
               'da6c5d8a-ce13-474d-9375-61feb29039a5': 'work_musicbrainz_id',
               'dd182715-ca2b-4e4b-80b1-d21742fda0dc': 'release_musicbrainz_id',
               'dd9886f2-1dfe-4270-97db-283f6839a666': 'artist_musicbrainz_id',
               'e035ac25-a2ff-48a6-9fb6-077692c67241': 'release_group_musicbrainz_id',
               'e259a3f5-ce8e-45c1-9ef7-90ff7d0c7589': 'artist_musicbrainz_id',
               'e5e6a204-8f81-4b17-9b54-a73a1a6db2bb': 'event_musicbrainz_id',
               'e74a40e7-0f27-4e05-bdbd-eb10f5309472': 'record_label_musicbrainz_id',
               'e794f8ff-b77b-4dfe-86ca-83197146ef10': 'artist_musicbrainz_id',
               'eb10f8a0-0f4c-4dce-aa47-87bcb2bc42f3': 'release_musicbrainz_id',
               'ed6a7891-ce70-4e08-9839-1f2f62270497': 'artist_musicbrainz_id',
               'eeb9c319-9fde-4313-b76d-29db1576aad8': 'work_musicbrainz_id',
               'f30c29d3-a3f1-420d-9b6c-a750fd6bc2aa': 'release_musicbrainz_id',
               'f3b80a09-5ebf-4ad2-9c46-3e6bce971d1b': 'release_musicbrainz_id',
               'f8673e29-02a5-47b7-af61-dd4519328dd0': 'recording_musicbrainz_id',
               'fd3927ba-fd51-4fa9-bcc2-e83637896fe8': 'artist_musicbrainz_id',
               'fe16f2bd-d324-435a-8076-bcf43b805bd9': 'record_label_musicbrainz_id',
               'ffeaa74f-8295-45ee-a2f2-7c0cc1f73b1e': 'recording_musicbrainz_id',
               'fff4640a-0819-49e9-92c5-1e3b5134fd95': 'place_musicbrainz_id'}})
@musicbrainz_feature
@timing_feature
def artist_relationships(artist_musicbrainz_id) -> ['record_label_musicbrainz_id', 'release_group_musicbrainz_id', 'artist_musicbrainz_id', 'place_musicbrainz_id', 'event_musicbrainz_id', 'recording_musicbrainz_id', 'release_musicbrainz_id', 'work_musicbrainz_id', ]:
    """Return every relation among an artist an another musicbrainz entity.

       We specify the type of the arrival node by distinguishing the relationship type.
       Moreover, we specify the edge_type as the id of the relationship in musicbrainz.
    """
    relationships_found = []

    if artist_musicbrainz_id is not None:

        relationship_types = ['artist',
                              'label',
                              'place',
                              'event',
                              'recording',
                              'release',
                              'release-group',
                              'work', ]
        artist = musicbrainzngs.get_artist_by_id(artist_musicbrainz_id['value'], includes=[f"{t}-rels" for t in relationship_types])['artist']
        for t in relationship_types:

            try:
                k = f"{t}-relation-list" if t != 'release-group' else "release_group-relation-list"
                relationships_of_type_t = artist[k]
            except KeyError:
                continue

            for relationship in relationships_of_type_t:

                if relationship['direction'] == 'forward':

                    d = {'edge_type': relationship['type-id'],
                         'node_type': _node_type(t),
                         'value': relationship['target']}
                    relationships_found.append(d)

    return relationships_found


def _node_type(t):
    if t in ['area', 'artist', 'place', 'event', 'recording', 'release', 'work']:
        return f'{t}_musicbrainz_id'
    elif t == 'label':
        return 'record_label_musicbrainz_id'
    elif t == 'release-group':
        return 'release_group_musicbrainz_id'
