#!/usr/bin/env python
"""
@package package_generator
@file test_code_generator.py
@author Anthony Remazeilles
@brief test the code generator

Copyright (C) 2017 Tecnalia Research and Innovation
Distributed under the GNU GPL v3.
For full terms see https://www.gnu.org/licenses/gpl.txt

To run a single test, type:
python test_code_generator.py CodeGeneratorTest.test_apply_function
"""

import unittest
import os
import rospkg

from package_generator.package_xml_parser import PackageXMLParser
from package_generator.code_generator import CodeGenerator


class CodeGeneratorTest(unittest.TestCase):
    """
    tests for the code generator
    """

    def setUp(self):
        """
        Common initialization for all tester
        """
        file_content = ('<?xml version="1.0" encoding="UTF-8"?>' '\n'
                        '<package name="great_package" author="anthony" author_email="anthony@todo.todo" description="The extended package" license="TODO">' '\n'
                        '   <node name="node_extended" frequency="100.0">' '\n'
                        '       <publisher name="pub" type="std_msgs::Bool" description=""/>' '\n'
                        '       <publisher name="pub_second" type="std_msgs::String" description=""/>' '\n'
                        '       <subscriber name="sub_in" type="std_msgs::String" description="" />' '\n'
                        '       <serviceClient name="service_client" type="std_srvs::Trigger" description=""/>' '\n'
                        '       <serviceServer name="service_server" type="std_srvs::SetBool" description=""/>' '\n'
                        '       <parameter name="param_one" type="std::string" value="Empty" description=""/>'  '\n'
                        '       <parameter name="param_two" type="bool" value="1" description=""/>'  '\n'
                        '       <actionServer name="action_server" type="bride_tutorials::TriggerPublish" description=""/>' '\n'
                        '       <actionClient name="action_client" type="bride_tutorials::TriggerPublish" description=""/>' '\n'
                        '   </node>' '\n'
                        '<depend>std_msgs</depend>' '\n'
                        '<depend>std_srvs</depend>' '\n'
                        '<depend>bride_tutorials</depend>' '\n'
                        '</package>' '\n')

        print "File content: \n{}".format(file_content)

        self.dir_name = "/tmp/test_package_generator"
        if not os.path.exists(self.dir_name):
            print "Creating the repo {}".format(self.dir_name)
            os.makedirs(self.dir_name)

        filename = self.dir_name + "/node_spec.ros_package"
        with open(filename, 'w') as open_file:
            open_file.write(file_content)

        self.xml_parser = PackageXMLParser()
        self.xml_parser.load(filename)
        self.generator_ = CodeGenerator()
        self.generator_.set_xml_parser(self.xml_parser)
        self.generator_.reset_output_file()

        rospack = rospkg.RosPack()
        self.template_path_ = rospack.get_path('package_generator_templates')

    def test_apply_function(self):
        """
        To apply a function on a tag
        """
        filename = self.dir_name + "/template_test_apply_function.cpp"
        file_content = ('{forallpublisher}' '\n'
                        'name={name}' '\n'
                        'pkg={apply-get_package_type} ' '\n'
                        'type={apply-get_class_type}' '\n'
                        'in one line: {name}: {apply-get_python_type}' '\n'
                        'cpp path: {name}: {apply-get_cpp_path}' '\n'
                        'more tricky: {name}: {apply-get_cpp_path} {unknowntag}' '\n'
                        'more tricky: {name}: {apply-get_cpp_path} {apply-unknown}' '\n'
                        '\n'
                        '{endforallpublisher}')

        expected_output = (
                          "name=pub" "\n"
                          "pkg=std_msgs " "\n"
                          "type=Bool" "\n"
                          "in one line: pub: std_msgs.Bool" "\n"
                          "cpp path: pub: std_msgs/Bool" "\n"
                          "more tricky: pub: std_msgs/Bool {unknowntag}" "\n"
                          "more tricky: pub: std_msgs/Bool {apply-unknown}" "\n"
                          "" "\n"
                          "name=pub_second" "\n"
                          "pkg=std_msgs " "\n"
                          "type=String" "\n"
                          "in one line: pub_second: std_msgs.String" "\n"
                          "cpp path: pub_second: std_msgs/String" "\n"
                          "more tricky: pub_second: std_msgs/String {unknowntag}" "\n"
                          "more tricky: pub_second: std_msgs/String {apply-unknown}" "\n")

        with open(filename, 'w') as openfile:
            openfile.write(file_content)

        self.assertTrue(self.generator_.process_file(filename))
        # self.generator_.write_output_file()
        # print "To compare with \n{}".format(expected_output)

        for generated, groundtruth in zip(self.generator_.tmp_buffer_,
                                          expected_output.splitlines()):
            # print "Comparing |{}| with |{}|".format(generated, groundtruth)
            self.assertEqual(generated, groundtruth)


    def test_multi_line(self):
        """
        Test  the conversion of multi-line
        """
        filename = self.dir_name + "/template_test_multiple_line.cpp"
        file_content = ('hello {nodeName}' '\n'
                        '{forallpublisher}' '\n'
                        'if (component_data_.{name}_active)' '\n'
                        '  pub_.publish(component_data_.{name});' '\n'
                        '{endforallpublisher}' '\n'
                        )
        expected_output = (
                          "hello node_extended" "\n"
                          "if (component_data_.pub_active)" "\n"
                          "  pub_.publish(component_data_.pub);" "\n"
                          "if (component_data_.pub_second_active)" "\n"
                          "  pub_.publish(component_data_.pub_second);" "\n")

        with open(filename, 'w') as open_file:
            open_file.write(file_content)

        self.assertTrue(self.generator_.process_file(filename))
        for generated, groundtruth in zip(self.generator_.tmp_buffer_,
                                          expected_output.splitlines()):
            self.assertEqual(generated, groundtruth)

    def test_multi_line_bracket(self):
        """
        Test correct management of multi-line with bracket
        """
        filename = self.dir_name + "/template_test_multiple_line.cpp"
        file_content = ('hello {nodeName}' '\n'
                        '{forallpublisher}' '\n'
                        'if (component_data_.{name}_active)' '\n'
                        '{' '\n'
                        '   pub_.publish(component_data_.{name});' '\n'
                        '}' '\n'
                        '{endforallpublisher}' '\n'
                        )
        expected_output = (
                           "hello node_extended" "\n"
                           "if (component_data_.pub_active)" "\n"
                           "{" "\n"
                           "   pub_.publish(component_data_.pub);" "\n"
                           "}" "\n"
                           "if (component_data_.pub_second_active)" "\n"
                           "{" "\n"
                           "   pub_.publish(component_data_.pub_second);" "\n"
                           "}" "\n"
                           )
        with open(filename, 'w') as open_file:
            open_file.write(file_content)

        self.assertTrue(self.generator_.process_file(filename))
        for generated, groundtruth in zip(self.generator_.tmp_buffer_,
                                          expected_output.splitlines()):
            self.assertEqual(generated, groundtruth)

    def test_multi_tag_single_line(self):
        """
        An intersting reference to look at if needed
        http://stackoverflow.com/questions/17215400/python-format-string-unused-named-arguments
        """
        filename = self.dir_name + "/template_test_multiple_tag.cpp"

        file_content = ('Let us start !!!!' '\n'
                        'hello {nodeName}' '\n'
                        '    void update({nodeName}_data &data, {nodeName}_config config)' '\n'
                        'Bye Bye' '\n'
                        )
        expected_output = (
                          "Let us start !!!!" "\n"
                          "hello node_extended" "\n"
                          "    void update(node_extended_data &data, node_extended_config config)" "\n"
                          "Bye Bye" "\n")

        with open(filename, 'w') as openfile:
            openfile.write(file_content)

        self.assertTrue(self.generator_.process_file(filename))
        for generated, groundtruth in zip(self.generator_.tmp_buffer_,
                                          expected_output.splitlines()):
            self.assertEqual(generated, groundtruth)

    def test_if_condition(self):
        """
        @brief Test the if condition
        @param      self The object
        @return nothing
        """
        filename = self.dir_name + "/template_test_multiple_line.cpp"
        file_content = ('Let us start !!!!' '\n'
                        '{ifparam}' '\n'
                        '<build_depend>dynamic_reconfigure</build_depend>' '\n'
                        '<run_depend>dynamic_reconfigure</run_depend>' '\n'
                        '{endifparam}' '\n'
                        '{ifaction}' '\n'
                        '<build_depend>actionlib</build_depend>' '\n'
                        '<run_depend>actionlib</run_depend>' '\n'
                        '{endifaction}' '\n'
                        )
        expected_output = (
                          "Let us start !!!!" "\n"
                          "<build_depend>dynamic_reconfigure</build_depend>" "\n"
                          "<run_depend>dynamic_reconfigure</run_depend>" "\n"
                          "<build_depend>actionlib</build_depend>" "\n"
                          "<run_depend>actionlib</run_depend>" "\n"
                           )

        with open(filename, 'w') as openfile:
            openfile.write(file_content)

        self.assertTrue(self.generator_.process_file(filename))
        for generated, groundtruth in zip(self.generator_.tmp_buffer_,
                                          expected_output.splitlines()):
            self.assertEqual(generated, groundtruth)

    def test_complete_ros(self):
        """
        @brief Test the generation of a complete cpp ros file

        @param      self The object
        @return nothing
        """
        filename = self.template_path_ + '/templates/cpp_node_update/ros/src/node_ros.cpp'

        self.assertTrue(self.generator_.process_file(filename))

        output_file = self.dir_name + "/node_ros.cpp"
        self.generator_.write_output_file(output_file)

    def test_complete_cmake(self):
        """
        @brief Test generation of a complete cmake

        @param      self The object

        @return { description_of_the_return_value }
        """
        filename = self.template_path_ + '/templates/cpp_node_update/CMakeLists.txt'

        self.assertTrue(self.generator_.process_file(filename))

        output_file = self.dir_name + "/CMakeLists.txt"
        self.generator_.write_output_file(output_file)

    def test_complete_readme(self):
        """
        @brief Test generation of a complete readme

        @param      self The object

        @return { description_of_the_return_value }
        """
        filename = self.template_path_ + '/templates/cpp_node_update/README.md'

        self.assertTrue(self.generator_.process_file(filename))

        output_file = self.dir_name + "/README.md"
        self.generator_.write_output_file(output_file)

    def test_complete_package(self):
        """
        @brief Test the generation of a complete package

        @param      self The object

        @return nothing
        """
        filename = self.template_path_ + '/templates/cpp_node_update/package.xml'

        self.assertTrue(self.generator_.process_file(filename))

        output_file = self.dir_name + "/package.xml"
        self.generator_.write_output_file(output_file)


if __name__ == '__main__':
    print "test_code_generator -- begin"
    unittest.main()
    print "test_code_generator -- end"
